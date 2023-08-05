#!/usr/bin/env python
#
# test_compare_tables.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


from unittest import mock

import ukbparse.scripts.compare_tables as ukbct

from . import tempdir


def test_compare_tables_help():
    try:
        ukbct.main([])
    except SystemExit as e:
        assert e.code == 0
    with mock.patch('sys.argv', ['ukbparse_compare_tables']):
        try:
            ukbct.main()
        except SystemExit as e:
            assert e.code == 0


data1 = """
ID\tType\tDescription\tDataCoding\tNAValues\tRawLevels\tNewLevels\tParentValues\tChildValues\tClean
0\tSequence\tEncoded anonymised participant ID
3\tInteger\tVerbal interview duration
4\tInteger\tBiometrics duration
5\tInteger\tSample collection duration
6\tInteger\tConclusion duration
19\tCategorical (single)\tHeel ultrasound method\t100260
21\tCategorical (single)\tWeight method\t100261
23\tCategorical (single)\tSpirometry method\t100270
31\tCategorical (single)\tSex\t9
""".strip()


data2 = """
ID\tType\tDescription\tDataCoding\tNAValues\tRawLevels\tNewLevels\tParentValues\tChildValues\tClean
3\tInteger\tVerbal interview duration
5\tInteger\tSample collection duration
6\tInteger\tConclusion duration
19\tCategorical (single)\tHeel ultrasound method\t100260
23\tCategorical (single)\tSpirometry method\t100270
34\tInteger\tYear of birth
35\tCategorical (single)\tWas blood sampling attempted\t7
46\tInteger\tHand grip strength (left)
47\tInteger\tHand grip strength (right)
48\tContinuous\tWaist circumference
49\tContinuous\tHip circumference
50\tContinuous\tStanding height
52\tCategorical (single)\tMonth of birth\t8
53\tDate\tDate of attending assessment centre
""".strip()


def test_compare_tables():

    with tempdir():
        with open('vars1.tsv', 'wt') as f: f.write(data1)
        with open('vars2.tsv', 'wt') as f: f.write(data2)
        ukbct.main(['vars1.tsv', 'vars2.tsv'])
