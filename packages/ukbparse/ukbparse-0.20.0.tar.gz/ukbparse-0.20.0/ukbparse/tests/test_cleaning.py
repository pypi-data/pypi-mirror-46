#!/usr/bin/env python
#
# test_cleaning.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import warnings
import random
import string
import textwrap as tw

import multiprocessing as mp
from unittest import mock

import pytest

import numpy  as np
import pandas as pd

import ukbparse.loadtables as lt
import ukbparse.cleaning as cleaning
import ukbparse.custom as custom
import ukbparse.cleaning_functions as cfns

import ukbparse.importing as importing
import ukbparse.hierarchy as hierarchy

from . import tempdir, gen_test_data, gen_tables, clear_plugins


def test_remove():
    assert cfns.remove(0, ['a', 'b', 'c']) == []


def  test_keepVisits():           _test_keepVisits(False)
def  test_keepVisits_lowMemory(): _test_keepVisits(True)
def _test_keepVisits(lowMemory):
    # first,
    # last,
    # number

    with tempdir():

        gen_test_data(20, 10, 'data.txt', max_visits=10, start_var=50)
        vartable, proctable, cattable, _ = gen_tables(range(50, 60))

        dt, _ = importing.importData('data.txt',
                                     vartable,
                                     proctable,
                                     cattable,
                                     removeUnknown=False,
                                     lowMemory=lowMemory)

        # find a column with several visits
        for v in dt.variables:
            cols = dt.columns(v)
            if len(cols) > 5:
                break

        assert cfns.keepVisits(v, cols, 'first') == [cols[0]]
        assert cfns.keepVisits(v, cols, 'last')  == [cols[-1]]
        assert cfns.keepVisits(v, cols, 2)       == [cols[2]]
        assert cfns.keepVisits(v, cols, 3, 4)    == cols[3:5]


def  test_fillVisits():           _test_fillVisits(False)
def  test_fillVisits_lowMemory(): _test_fillVisits(True)
def _test_fillVisits(lowMemory):

    with tempdir(), mp.Pool(mp.cpu_count()) as pool:

        mgr = mp.Manager()

        data        = np.zeros((20, 4), dtype=np.float32)
        data[:, 0]  = np.arange(1, 21)
        data[:, 1:] = np.random.randint(1, 100, (20, 3))

        cols = ['eid', '1-0.0', '1-1.0', '1-2.0']

        data[ 0:10, 1] = np.nan
        data[ 5:15, 2] = np.nan
        data[10:,   3] = np.nan

        meanexp           = np.copy(data)
        meanexp[ 0:5,  1] = np.mean(data[0:5, 2:4], axis=1)
        meanexp[ 5:10, 1] = data[ 5:10, 3]
        meanexp[ 5:10, 2] = data[ 5:10, 3]
        meanexp[10:15, 2] = data[10:15, 1]
        meanexp[10:15, 3] = data[10:15, 1]
        meanexp[15:20, 3] = np.mean(data[15:20, 1:3], axis=1)

        modeexp           = np.copy(meanexp)

        m1 = pd.DataFrame({'a' : data[ 0:5,  2], 'b' : data[ 0:5,  3]})
        m1 = np.asarray(m1.mode(axis=1).iloc[:, 0])

        m2 = pd.DataFrame({'a' : data[15:20, 1], 'b' : data[15:20, 2]})
        m2 = np.asarray(m2.mode(axis=1).iloc[:, 0])

        modeexp[ 0:5,  1] = m1
        modeexp[15:20, 3] = m2

        with open('data.txt', 'wt') as f:

            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')

        vartable, proctable, cattable, _ = gen_tables([1])

        for method in ['mean', 'mode']:

            dt, _ = importing.importData('data.txt',
                                         vartable,
                                         proctable,
                                         cattable,
                                         removeUnknown=False,
                                         lowMemory=lowMemory,
                                         pool=pool,
                                         mgr=mgr)

            cfns.fillVisits(dt, 1, method)

            if   method == 'mean': exp = meanexp
            elif method == 'mode': exp = modeexp

            assert np.all(dt[:, '1-0.0'] == exp[:, 1])
            assert np.all(dt[:, '1-1.0'] == exp[:, 2])
            assert np.all(dt[:, '1-2.0'] == exp[:, 3])

        with pytest.raises(ValueError):
            cfns.fillVisits(dt, 1, 'bad_method')
        dt = None
        mgr = None
        pool = None


def  test_fillMissing():           _test_fillMissing(False)
def  test_fillMissing_lowMemory(): _test_fillMissing(True)
def _test_fillMissing(lowMemory):
    with tempdir(), mp.Pool(mp.cpu_count()) as pool:

        mgr = mp.Manager()

        data        = np.zeros((20, 3), dtype=np.float32)
        data[:, 0]  = np.arange(1, 21)
        data[:, 1:] = np.random.randint(1, 100, (20, 2))

        cols = ['eid', '1-0.0', '2-0.0']

        data[ 0:10, 1] = np.nan
        data[ 5:15, 2] = np.nan

        exp = np.copy(data)
        exp[ 0:10, 1] = 999
        exp[ 5:15, 2] = 12345

        with open('data.txt', 'wt') as f:

            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')

        vartable, proctable, cattable, _ = gen_tables([1])

        dt, _ = importing.importData('data.txt',
                                     vartable,
                                     proctable,
                                     cattable,
                                     removeUnknown=False,
                                     lowMemory=lowMemory,
                                     pool=pool,
                                     mgr=mgr)

        cfns.fillMissing(dt, 1, 999)
        cfns.fillMissing(dt, 2, 12345)

        assert np.all(dt[:, '1-0.0'] == exp[:, 1])
        assert np.all(dt[:, '2-0.0'] == exp[:, 2])
        dt = None
        mgr = None
        pool = None


def  test_convertICD10Codes():           _test_convertICD10Codes(False)
def  test_convertICD10Codes_lowMemory(): _test_convertICD10Codes(True)
def _test_convertICD10Codes(lowMemory):

    icd10hier = hierarchy.getHierarchyFilePath(name='icd10')
    icd10hier = hierarchy.loadHierarchyFile(icd10hier)
    codes     = list(random.sample(icd10hier.codings, 20)) + ['badcode']
    exp       = [icd10hier.index(c) + 1 for c in codes[:-1]] + [np.nan]

    with tempdir(), mp.Pool(mp.cpu_count()) as pool:
        mgr = mp.Manager()
        with open('data.txt', 'wt') as f:
            f.write('eid\t1-0.0\n')
            for i, c in enumerate(codes, 1):
                f.write('{}\t{}\n'.format(i, c))


        vartable, proctable, cattable, _ = gen_tables([1])

        dt, _ = importing.importData('data.txt',
                                     vartable,
                                     proctable,
                                     cattable,
                                     removeUnknown=False,
                                     lowMemory=lowMemory,
                                     pool=pool,
                                     mgr=mgr)
        cfns.convertICD10Codes(dt, 1)

        got = dt[:, '1-0.0']
        exp = pd.Series(exp, name='1-0.0', index=got.index)

        gotna = pd.isna(got)
        expna = pd.isna(exp)

        assert np.all(got[~gotna] == exp[~expna])
        assert np.all(gotna       == expna)
        dt = None
        mgr = None
        pool = None


def  test_makeNa():           _test_makeNa(False)
def  test_makeNa_lowMemory(): _test_makeNa(True)
def _test_makeNa(lowMemory):

    data        = np.zeros((100, 3), dtype=np.float32)
    data[:, 0]  = np.arange(1, 101)
    data[:, 1:] = np.random.randint(1, 100, (100, 2))

    cols = ['eid', '1-0.0', '2-0.0']

    with tempdir(), mp.Pool(mp.cpu_count()) as pool:

        mgr = mp.Manager()
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')
        vartable, proctable, cattable, _ = gen_tables([1, 2])

        dt, _ = importing.importData('data.txt',
                                     vartable,
                                     proctable,
                                     cattable,
                                     removeUnknown=False,
                                     lowMemory=lowMemory,
                                     pool=pool,
                                     mgr=mgr)

        cfns.makeNa(dt, 1, '>= 25')
        cfns.makeNa(dt, 2, '<  50')

        na1mask = data[:, 1] >= 25
        na2mask = data[:, 2] <  50

        dt1 = dt[dt[:, '1-0.0'].notna(), '1-0.0']
        dt2 = dt[dt[:, '2-0.0'].notna(), '2-0.0']

        assert np.all(      na1mask     == dt[:, '1-0.0'].isna())
        assert np.all(      na2mask     == dt[:, '2-0.0'].isna())
        assert np.all(data[~na1mask, 1] == dt1)
        assert np.all(data[~na2mask, 2] == dt2)
        dt = None
        mgr = None
        pool = None


def  test_applyNewLevels():           _test_applyNewLevels(False)
def  test_applyNewLevels_lowMemory(): _test_applyNewLevels(True)
def _test_applyNewLevels(lowMemory):

    data       = np.random.randint(0, 10, (50, 3))
    data[:, 0] = np.arange(1, 51)

    codes1 = np.random.randint(100, 200, 10)
    codes2 = np.random.randint(100, 200, 10)

    exp1 = [codes1[data[i, 1]] for i in range(50)]
    exp2 = [codes2[data[i, 2]] for i in range(50)]

    vartable, proctable, cattable, _ = gen_tables([1, 2, 3])

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        vartable['RawLevels'][1] = list(range(10))
        vartable['NewLevels'][1] = codes1
        vartable['RawLevels'][2] = list(range(10))
        vartable['NewLevels'][2] = codes2
        vartable['RawLevels'][3] = list(range(10))
        vartable['NewLevels'][3] = codes2


    cols = ['eid', '1-0.0', '2-0.0']

    with tempdir(), mp.Pool(mp.cpu_count()) as pool:

        mgr = mp.Manager()
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')

        dt, _ = importing.importData('data.txt',
                                     vartable,
                                     proctable,
                                     cattable,
                                     removeUnknown=False,
                                     lowMemory=lowMemory,
                                     pool=pool,
                                     mgr=mgr)

        cleaning.applyNewLevels(dt)
        assert np.all(dt[:, '1-0.0'] == exp1)
        assert np.all(dt[:, '2-0.0'] == exp2)
        dt = None
        mgr = None
        pool = None



def  test_applyNAInsertion():           _test_applyNAInsertion(False)
def  test_applyNAInsertion_lowMemory(): _test_applyNAInsertion(True)
def _test_applyNAInsertion(lowMemory):

    data       = np.random.randint(0, 10, (100, 3)).astype(np.float32)
    data[:, 0] = np.arange(1, 101)

    miss1 = list(np.random.choice(range(10), 4, replace=False))
    miss2 = list(np.random.choice(range(10), 4, replace=False))

    exp1 = data[:, 1].copy()
    exp2 = data[:, 2].copy()

    for m in miss1: exp1[exp1 == m] = np.nan
    for m in miss2: exp2[exp2 == m] = np.nan

    vartable, proctable, cattable, _ = gen_tables([1, 2, 3])

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        vartable['NAValues'][1] = miss1
        vartable['NAValues'][2] = miss2
        vartable['NAValues'][3] = [1, 2, 3]

    cols = ['eid', '1-0.0', '2-0.0']

    with tempdir(), mp.Pool(mp.cpu_count()) as pool:

        mgr = mp.Manager()
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')

        dt, _ = importing.importData('data.txt',
                                     vartable,
                                     proctable,
                                     cattable,
                                     removeUnknown=False,
                                     lowMemory=lowMemory,
                                     pool=pool,
                                     mgr=mgr)

        cleaning.applyNAInsertion(dt)

        na1mask = dt[:, '1-0.0'].isna()
        na2mask = dt[:, '2-0.0'].isna()

        d1 = dt[:, '1-0.0'][~na1mask]
        d2 = dt[:, '2-0.0'][~na2mask]

        assert np.all(na1mask == np.isnan(exp1))
        assert np.all(na2mask == np.isnan(exp2))

        assert np.all(d1 == exp1[~na1mask])
        assert np.all(d2 == exp2[~na2mask])
        dt = None
        mgr = None
        pool = None


def  test_applyChildValues():           _test_applyChildValues(False)
def  test_applyChildValues_lowMemory(): _test_applyChildValues(True)
def _test_applyChildValues(lowMemory):

    sz          = 100
    data        = np.zeros((sz, 6), dtype=np.float32)
    data[:, 0]  = np.arange(1, sz + 1)
    data[:, 1:] = np.random.randint(1, 10, (sz, 5))

    cols = ['eid', '1-0.0', '2-0.0', '3-0.0', '4-0.0', '5-0.0']

    # parents
    # 1: 2, 3
    # 2: 3
    # 3: 4
    # 4: 5

    pvals = {
        1 : 'v2 == 5, v3 > 5',
        2 : 'v3 < 8',
        3 : 'v4 >= 6',
        4 : 'v5 == 2',
        5 : 'v123 == 7',
        6 : 'v8 < 5'
    }
    cvals = {
        1 : '100, 101',
        2 : '200',
        3 : '300',
        4 : '400',
        5 : '123',
        6 : '1234'
    }

    data[ data[:, 5] == 2,                     4] = np.nan
    data[ data[:, 4] >= 6,                     3] = np.nan
    data[ data[:, 3] <  8,                     2] = np.nan
    data[(data[:, 2] == 5) | (data[:, 3] > 5), 1] = np.nan

    exp  = np.copy(data)
    nan1 = np.isnan(exp[:, 1])
    exp[    nan1            & (exp[:, 2] == 5), 1] = 100
    exp[    nan1            & (exp[:, 3] >  5), 1] = 101
    exp[np.isnan(exp[:, 2]) & (exp[:, 3] <  8), 2] = 200
    exp[np.isnan(exp[:, 3]) & (exp[:, 4] >= 6), 3] = 300
    exp[np.isnan(exp[:, 4]) & (exp[:, 5] == 2), 4] = 400

    with tempdir(), mp.Pool(mp.cpu_count()) as pool:

        mgr = mp.Manager()
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')

        vartable, proctable, cattable, _ = gen_tables([1, 2, 3, 4, 5, 6])

        vartable.loc[pvals.keys(), 'ParentValues'] = \
            [lt.convert_ParentValues(v) for v in pvals.values()]
        vartable.loc[cvals.keys(), 'ChildValues'] = \
            [lt.convert_comma_sep_numbers(v) for v in cvals.values()]

        dt, _ = importing.importData('data.txt',
                                     vartable,
                                     proctable,
                                     cattable,
                                     removeUnknown=False,
                                     lowMemory=lowMemory,
                                     pool=pool,
                                     mgr=mgr)

        cleaning.applyChildValues(dt)

        assert np.all(np.asarray(dt[:, :].values) == exp[:, 1:])
        dt = None
        mgr = None
        pool = None


@clear_plugins
def  test_applyCleaningFunctions():           _test_applyCleaningFunctions(False)
def  test_applyCleaningFunctions_lowMemory(): _test_applyCleaningFunctions(True)
def _test_applyCleaningFunctions(lowMemory):

    data        = np.zeros((100, 3), dtype=np.float32)
    data[:, 0]  = np.arange(1, 101)
    data[:, 1:] = np.random.randint(1, 100, (100, 2))

    cols = ['eid', '1-0.0', '2-0.0']

    @custom.cleaner()
    def proc1(dtable, vid):
        columns = dtable.columns(vid)
        for c in columns:
            dtable[:, c.name] = dtable[:, c.name] + 5


    @custom.cleaner()
    def proc2(dtable, vid, factor):
        columns = dtable.columns(vid)
        for c in columns:
            dtable[:, c.name] = dtable[:, c.name] * factor


    with tempdir(), mp.Pool(mp.cpu_count()) as pool:

        mgr = mp.Manager()
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')
        vartable, proctable, cattable, _ = gen_tables([1, 2, 3])

        vartable.loc[(1, ), 'Clean'] = (lt.convert_Process(
            'cleaner', 'proc1'), )
        vartable.loc[(2, ), 'Clean'] = (lt.convert_Process(
            'cleaner', 'proc2(50)'), )
        vartable.loc[(3, ), 'Clean'] = (lt.convert_Process(
            'cleaner', 'proc2(50)'), )

        dt, _ = importing.importData('data.txt',
                                     vartable,
                                     proctable,
                                     cattable,
                                     removeUnknown=False,
                                     pool=pool,
                                     mgr=mgr)

        cleaning.applyCleaningFunctions(dt)

        assert np.all(dt[:, '1-0.0'] == data[:, 1] + 5)
        assert np.all(dt[:, '2-0.0'] == data[:, 2] * 50)
        dt = None
        mgr = None
        pool = None


def test_cleanData():

    data        = np.zeros((100, 3), dtype=np.float32)
    data[:, 0]  = np.arange(1, 101)
    data[:, 1:] = np.random.randint(1, 100, (100, 2))

    cols = ['eid', '1-0.0', '2-0.0']

    with tempdir(), mp.Pool(mp.cpu_count()) as pool:

        mgr = mp.Manager()
        custom.registerBuiltIns()
        with open('data.txt', 'wt') as f:
            f.write('\t'.join(cols) + '\n')
            np.savetxt(f, data, delimiter='\t')
        vartable, proctable, cattable, _ = gen_tables([1, 2])
        dt, _ = importing.importData('data.txt',
                                     vartable,
                                     proctable,
                                     cattable,
                                     removeUnknown=False,
                                     pool=pool,
                                     mgr=mgr)

        # not crashing -> pass
        cleaning.cleanData(dt)
        dt = None
        mgr = None
        pool = None


def  test_parseSpirometryData_lowMemory(): _test_parseSpirometryData(True)
def  test_parseSpirometryData():           _test_parseSpirometryData(False)
def _test_parseSpirometryData(lowMemory):

    data = tw.dedent("""
    eid\t1-0.0\t1-0.1\t1-0.2
    1\tblow1,5,1,2,3,4,5\tblow2,3,4,5,6\tblow3,6,1,2,3,4,5,6
    2\tblow2,5,1,2,3,4,5\tblow3,5,5,4,3,2,1\tblow1,3,3,2,1
    3\tblow1,5,1,2,3,4,5\tblow3,4,6,7,8,9\tblow2,2,1,2
    """).strip()

    # arranged by column
    exp = [
        [[1, 2, 3, 4, 5],    [3, 2, 1],       [1, 2, 3, 4, 5]],
        [[4, 5, 6],          [1, 2, 3, 4, 5], [1, 2]],
        [[1, 2, 3, 4, 5, 6], [5, 4, 3, 2, 1], [6, 7, 8, 9]]]

    exp = [[np.array(row) for row in col] for col in exp]
    exp = [pd.Series(col) for col in exp]

    with tempdir(), mp.Pool(mp.cpu_count()) as pool:
        with open('data.txt', 'wt') as f:
            f.write(data)

        mgr = mp.Manager()
        vartable, proctable, cattable, _ = gen_tables([1, 2])

        dt, _ = importing.importData('data.txt',
                                     vartable,
                                     proctable,
                                     cattable,
                                     removeUnknown=False,
                                     lowMemory=lowMemory,
                                     pool=pool,
                                     mgr=mgr)

        cfns.parseSpirometryData(dt, 1)

        for coli, col in enumerate(['1-0.0', '1-0.1', '1-0.2']):
            got = dt[:, col]

            for rowi in range(len(got)):
                assert np.all(exp[coli][rowi] == got.iloc[rowi])
        dt = None
        mgr = None
        pool = None


def  test_flattenHierarchical_lowMemory(): _test_flattenHierarchical(True)
def  test_flattenHierarchical():           _test_flattenHierarchical(False)
def _test_flattenHierarchical(lowMemory):

    data = tw.dedent("""
    eid,1-0.0
    1,10
    2,20
    3,30
    4,40
    5,50
    6,60
    7,70
    8,80
    9,90
    """).strip()

    hier = tw.dedent("""
    coding	meaning	node_id	parent_id
    10	meaning 10	1	0
    20	meaning 20	2	0
    30	meaning 30	3	1
    40	meaning 40	4	1
    50	meaning 50	5	4
    60	meaning 60	6	2
    70	meaning 70	7	2
    80	meaning 80	8	6
    90	meaning 90	9	8
    """).strip()

    tests = [
        (0, [10, 20, 10, 10, 10, 20, 20, 20, 20]),
        (1, [10, 20, 30, 40, 40, 60, 70, 60, 60]),
        (2, [10, 20, 30, 40, 50, 60, 70, 80, 80]),
        (3, [10, 20, 30, 40, 50, 60, 70, 80, 90]),
        (4, [10, 20, 30, 40, 50, 60, 70, 80, 90]),
    ]

    with tempdir(), mp.Pool(mp.cpu_count()) as pool:

        with open('data.txt', 'wt') as f:
            f.write(data)

        with open('hier.txt', 'wt') as f:
            f.write(hier)

        mgr = mp.Manager()
        vartable, proctable, cattable, _ = gen_tables([1])

        for level, exp in tests:

            dt, _ = importing.importData('data.txt',
                                         vartable,
                                         proctable,
                                         cattable,
                                         removeUnknown=False,
                                         lowMemory=lowMemory,
                                         pool=pool,
                                         mgr=mgr)

            with mock.patch('ukbparse.hierarchy.getHierarchyFilePath',
                            return_value='hier.txt'):
                cfns.flattenHierarchical(dt, 1, level)

            assert np.all(dt[:, '1-0.0'].values == exp)

        dt = None
        mgr = None
        pool = None
