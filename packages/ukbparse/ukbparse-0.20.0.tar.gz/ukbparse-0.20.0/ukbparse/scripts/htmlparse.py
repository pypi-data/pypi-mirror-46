#!/usr/bin/env python
#
# htmlparse.py - Parse UKBiobank HTML metadata files.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This script parses the HTML files generated by the UK BioBank ``ukbconv``
utility.

The output of this script are variable and data coding base files, which
can be used as a base for generating variable and data coding tables to be
used by ``ukbparse``.

The script can be used as follows::

    python scripts/htmlparse.py file.html [file.html ...] \\
        datacodings_base.tsv varlables_base.tsv

See also the ``ukbparse_join`` command.
"""


import sys
from collections import OrderedDict

import bs4


def parse_data_codings(fpath):
    with open(fpath, 'rt', encoding='latin_1') as f:
        soup = bs4.BeautifulSoup(f, 'lxml')

    datacodings = soup.find_all('table')
    datacodings = [dc for dc in datacodings
                   if dc.get('summary', '').startswith('Coding')]

    parsed = OrderedDict()

    for dc in datacodings:
        cid    = int(dc['summary'].split()[-1])
        values = dc.find_all('td')

        meanings = values[2::3]
        values   = values[1::3]

        values   = [str(v.string) for v in values]
        meanings = [str(m.string) for m in meanings]

        codes = OrderedDict()
        ctype = None

        for v, m in zip(values, meanings):
            try:
                codes[int(v)] = m
            except ValueError:
                if 'not selectable' in v:
                    continue
                codes[v] = m
                ctype = str
        parsed[cid] = ctype, codes

    return parsed


def gen_data_coding_table(datacodings, fpath):

    columns = ['ID']

    with open(fpath, 'wt') as f:
        f.write('\t'.join(columns) + '\n')

        for cid in sorted(datacodings.keys()):

            # id
            row = [str(cid)]

            f.write('\t'.join(row) + '\n')


def parse_variables(fpath):
    print('parsing', fpath)
    with open(fpath, 'rt', encoding='latin_1') as f:
        soup = bs4.BeautifulSoup(f, 'lxml')

    vartable = soup    .find_all('table')[1]
    varrows  = vartable.find_all('tr')[   1:]

    vids    = []
    nvisits = []
    nitems  = []
    codings = []
    types   = []
    descs   = []

    def split_udi(udi):
        vid   = int(udi.split('-')[0])
        udi   = udi[udi.find('-') + 1:]
        visit = int(udi.split('.')[0])
        item  = int(udi.split('.')[1])
        return vid, visit, item

    i = 0
    while i < len(varrows):

        # column 0: row index
        # column 1: UDI
        # column 2: count

        # Remaining columns are only present on the
        # first visit/item for a given variable

        # column 3: type
        # column 4: description (and maybe data coding)

        cols   = varrows[i].find_all('td')
        # in newer versions of the HTML format,
        # the eid column name is not a href
        if cols[1].a is not None: udi = str(cols[1].a.string)
        else:                     udi = str(cols[1]  .string)

        vtype  = str(cols[3].span.string)
        desc   = str(cols[4].contents[0])

        if vtype == 'Curve':
            vtype = 'Compound'

        try:
            coding = int(cols[4].contents[3].string)
        except Exception:
            coding = None

        if i == 0:
            i     +=  1
            vid    =  0
            visits = [0]
            items  = [0]

        # Fast-forward rows, count items/visits
        else:
            i += 1
            vid, visit, item = split_udi(udi)
            visits = [visit]
            items  = [item]

            for i in range(i, len(varrows) + 1):
                if i == len(varrows):
                    break
                udi   = str(varrows[i].find_all('td')[1].a.string)
                vvid, visit, item = split_udi(udi)

                # same variable, different visit/item
                if vvid == vid:
                    visits.append(visit)
                    items .append(item)
                    continue

                # new variable
                else:
                    break

            # sanity check - same number
            # of items for each visit
            byvisit   = OrderedDict()
            uniqitems = []
            for visit, item in zip(visits, items):
                if visit not in byvisit:
                    byvisit[visit] = []
                byvisit[visit].append(item)
                if item not in uniqitems:
                    uniqitems.append(item)

            for vi in byvisit.values():
                assert vi == uniqitems

        vids   .append(vid)
        nvisits.append(visits)
        nitems .append(items)
        codings.append(coding)
        types  .append(vtype)
        descs  .append(desc)

    return vids, nvisits, nitems, codings, types, descs


def gen_variable_coding_table(varcodings, fpath):

    columns = ['ID', 'Type', 'Description', 'DataCoding']

    # sort by vid
    byvid = {}
    for vid, nvisits, nitems, coding, vtype, desc in varcodings:
        byvid[vid] = (nvisits, nitems, coding, vtype, desc)

    vids    = sorted(byvid.keys())
    nvisits = [byvid[vid][0] for vid in vids]
    nitems  = [byvid[vid][1] for vid in vids]
    codings = [byvid[vid][2] for vid in vids]
    types   = [byvid[vid][3] for vid in vids]
    descs   = [byvid[vid][4] for vid in vids]

    with open(fpath, 'wt') as f:
        f.write('\t'.join(columns) + '\n')
        for i, (vid, coding, vtype, desc) in enumerate(
                zip(vids, codings, types, descs)):

            if coding is None:
                coding = ''

            row = []
            row.append(str(vid))
            row.append(str(vtype))
            row.append(str(desc))
            row.append(str(coding))

            f.write('\t'.join(row) + '\n')


def main(args=None):

    print('WARNING: htmlparse.py is deprecated and will be removed in a '
          'future version of ukbparse. Variable and datacoding information '
          'is now stored in the ukbparse/data/field.txt and ukbparse/data/'
          'encoding.txt files. Updated copies of these files can be obtained '
          'from https://biobank.ctsu.ox.ac.uk/crystal/schema.cgi')
    print()

    if args is None:
        args = sys.argv[1:]

    if len(args) < 3:
        print('Usage: htmlparse.py file.html [file.html ...] '
              'datacodings_base.tsv variables_base.tsv')
        print()
        print(__doc__)
        sys.exit(0)

    infiles       = args[:-2]
    datacodingout = args[-2]
    varcodingout  = args[-1]

    datacodings = OrderedDict()
    varcodings  = []

    vids = set()

    for inf in infiles:
        dcs = parse_data_codings(inf)
        vcs = parse_variables(   inf)

        for i, vc in enumerate(zip(*vcs)):
            if vc[0] not in vids:
                vids.add(vc[0])
                varcodings.append(vc)

                vdc = vc[3]

                if vdc is not None and vdc not in dcs:
                    print('WARNING: Variable {} uses data coding {}, but '
                          'the latter is not described!'.format(vc[0], vdc))

            else:
                print('WARNING: Dropping duplicate variable '
                      'from {}: {} [{}...]'.format(inf, vc[0], vc[5][:50]))

        datacodings.update(dcs)

    gen_data_coding_table(    datacodings, datacodingout)
    gen_variable_coding_table(varcodings,  varcodingout)


if __name__ == '__main__':
    main()
