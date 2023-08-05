#!/usr/bin/env python
#
# test_htmlparse.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


from unittest import mock

import ukbparse.scripts.htmlparse as ukbhp

from . import tempdir


testfile  = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
<style type="text/css">
body {font-family: Arial, Verdana, sans-serif; }
a:link {text-decoration: none; }
td {vertical-align: top;}
</style>
<title>UK Biobank : Application 8107</title>
</head>
<body>
<h1>UK Biobank : Data Dictionary for Application 8107</h1>
<p>
<table>
<tr><td>Date Extracted:</td><td>2018-08-08T09:55:12</td></tr>
<tr><td>Data columns:</td><td>13976</td></tr>
</table>
<!-- Extraction version: V5 Created by REX: 2018-08-08T09:55:12 -->
<!-- Basket ID: 8251 -->
<!-- Run ID: 23261 -->
<!-- Ukb2docs compiled: Jun 21 2016 10:29:39 -->
<p>
<table border cellspacing="0">
<tr><th>Column</th><th><a href="#udi">UDI</a></th><th><a href="#count">Count</a></th><th>Type</th><th>Description</th></tr>
<tr><td style="text-align: right;">0</td><td><a href="http://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=0">eid</a></td><td style="text-align: right;">502591</td><td rowspan="1"><span style="white-space: nowrap;">Sequence</span></td><td rowspan="1">Encoded anonymised participant ID</td></tr>
<tr><td style="text-align: right;">1</td><td><a href="http://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=3">3-0.0</a></td><td style="text-align: right;">501729</td><td rowspan="3"><span style="white-space: nowrap;">Integer</span></td><td rowspan="3">Verbal interview duration</td></tr>
<tr><td style="text-align: right;">13</td><td><a href="http://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=19">19-0.0</a></td><td style="text-align: right;">324833</td><td rowspan="1"><span style="white-space: nowrap;">Categorical (single)</span></td><td rowspan="1">Heel ultrasound method<br>Uses data-coding <a href="http://biobank.ctsu.ox.ac.uk/crystal/coding.cgi?id=100260">100260</a> comprises 5 Integer-valued members in a simple list.</td></tr>
<tr><td style="text-align: right;">14</td><td><a href="http://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=21">21-0.0</a></td><td style="text-align: right;">500876</td><td rowspan="3"><span style="white-space: nowrap;">Categorical (single)</span></td><td rowspan="3">Weight method<br>Uses data-coding <a href="http://biobank.ctsu.ox.ac.uk/crystal/coding.cgi?id=100261">100261</a> comprises 5 Integer-valued members in a simple list.</td></tr>
</table>
<h3>Data-Coding 100260</h3>
 comprises 5 Integer-valued members in a simple list.
<table border cellspacing="0" summary="Coding 100260">
<tr><th>#</th><th>Code</th><th>Meaning</th>
<tr><td>1</td><td>1</td><td>Direct entry</td></tr>
<tr><td>2</td><td>2</td><td>Manual entry</td></tr>
<tr><td>3</td><td>6</td><td>Not performed - equipment failure</td></tr>
<tr><td>4</td><td>7</td><td>Not performed - other reason</td></tr>
<tr><td>5</td><td>3</td><td>Not performed</td></tr>
</table>
<h3>Data-Coding 100261</h3>
 comprises 5 Integer-valued members in a simple list.
<table border cellspacing="0" summary="Coding 100261">
<tr><th>#</th><th>Code</th><th>Meaning</th>
<tr><td>1</td><td>1</td><td>Direct entry</td></tr>
<tr><td>2</td><td>2</td><td>Manual entry of full results</td></tr>
<tr><td>3</td><td>3</td><td>Manual measurement of weight only</td></tr>
<tr><td>4</td><td>4</td><td>Not performed</td></tr>
<tr><td>5</td><td>-1</td><td>Question not asked due to previous answers</td></tr>
</table>
<h3>Data-Coding 100270</h3>
 comprises 5 Integer-valued members in a simple list.
<table border cellspacing="0" summary="Coding 100270">
<tr><th>#</th><th>Code</th><th>Meaning</th>
<tr><td>1</td><td>0</td><td>Direct entry</td></tr>
<tr><td>2</td><td>1</td><td>Manual</td></tr>
<tr><td>3</td><td>6</td><td>Not performed - equipment failure</td></tr>
<tr><td>4</td><td>7</td><td>Not performed - other reason</td></tr>
<tr><td>5</td><td>9</td><td>Cannot be measured</td></tr>
</table>
<hr>
END</body>
</html>
""".strip()


expvarbase = """
ID\tType\tDescription\tDataCoding
0\tSequence\tEncoded anonymised participant ID\t
3\tInteger\tVerbal interview duration\t
19\tCategorical (single)\tHeel ultrasound method\t100260
21\tCategorical (single)\tWeight method\t100261
""".strip()


expdcbase = """
ID
100260
100261
100270
""".strip()



def test_htmlparse_help():
    try:
        ukbhp.main([])
    except SystemExit as e:
        assert e.code == 0
    with mock.patch('sys.argv', ['ukbparse_htmlparse']):
        try:
            ukbhp.main()
        except SystemExit as e:
            assert e.code == 0


def test_htmlparse():
    with tempdir():
        with open('infile.html', 'wt') as f:
            f.write(testfile)

        ukbhp.main(['infile.html', 'dc_base.tsv', 'var_base.tsv'])

        with open('dc_base.tsv',  'rt') as f: gotdcbase  = f.read().strip()
        with open('var_base.tsv', 'rt') as f: gotvarbase = f.read().strip()

        assert gotdcbase  == expdcbase
        assert gotvarbase == expvarbase
