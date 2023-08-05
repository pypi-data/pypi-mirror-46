#!/usr/bin/env python
#
# test_join.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

from unittest import mock

import textwrap as tw

import ukbparse.scripts.join as ukbjoin

from . import tempdir


def test_join_no_args():

    try:
        ukbjoin.main([])
    except SystemExit as e:
        assert e.code == 0

    with mock.patch('sys.argv', ['ukbparse_join']):
        try:
            ukbjoin.main()
        except SystemExit as e:
            assert e.code == 0



def test_join():

    file1 = tw.dedent("""
    ID\tType\tDescription
    1\t10\t100
    2\t20\t200
    3\t30\t300
    4\t40\t400
    5\t\t
    6\t\t
    7\t\t
    8\t\t
    """).strip()

    file2 = tw.dedent("""
    ID\tNAValues\tDataCoding
    2\t2000\t20000
    4\t4000\t40000
    6\t6000\t60000
    8\t8000\t80000
    """).strip()

    exp1 = tw.dedent("""
    ID\tType\tDescription\tNAValues\tDataCoding
    1\t10\t100\t\t
    2\t20\t200\t2000\t20000
    3\t30\t300\t\t
    4\t40\t400\t4000\t40000
    5\t\t\t\t
    6\t\t\t6000\t60000
    7\t\t\t\t
    8\t\t\t8000\t80000
    """).strip()

    exp2 = tw.dedent("""
    ID\tNAValues\tDataCoding\tType\tDescription
    2\t2000\t20000\t20\t200
    4\t4000\t40000\t40\t400
    6\t6000\t60000\t\t
    8\t8000\t80000\t\t
    """).strip()

    with tempdir():

        with open('file1.txt', 'wt') as f: f.write(file1)
        with open('file2.txt', 'wt') as f: f.write(file2)

        ukbjoin.main(['out1.txt', 'file1.txt', 'file2.txt'])
        ukbjoin.main(['out2.txt', 'file2.txt', 'file1.txt'])

        with open('out1.txt', 'rt') as f: assert f.read().strip() == exp1
        with open('out2.txt', 'rt') as f: assert f.read().strip() == exp2
