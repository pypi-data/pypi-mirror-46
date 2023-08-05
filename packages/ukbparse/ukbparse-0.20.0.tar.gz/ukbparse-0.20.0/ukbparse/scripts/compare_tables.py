#!/usr/bin/env python
#
# compare_tables.py - Comapre datacoding/variable tables
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""Compare new data coding/variable tables with old ones.

When the data coding/variable tables are re-generated from new Biobank data
releases, this script can be used to compare the old versions with the new
ones to see what has changed.
"""

import sys

import pandas as pd


def compare(fold, fnew):

    dold = pd.read_csv(fold, delimiter='\t', index_col=0)
    dnew = pd.read_csv(fnew, delimiter='\t', index_col=0)

    iold = dold.index
    inew = dnew.index

    old_minus_new = sorted(set(iold).difference(  set(inew)))
    new_minus_old = sorted(set(inew).difference(  set(iold)))
    old_and_new   = sorted(set(iold).intersection(set(inew)))

    print('# old       ', len(iold))
    print('# new       ', len(inew))
    print('# old - new ', len(old_minus_new))
    print('# new - old ', len(new_minus_old))

    print()
    print('all old - new')
    for i in old_minus_new:
        print('  {}: [navalues {}] [rawlevels {}] [newlevels {}]'.format(
              i,
              dold['NAValues'][i],
              dold['RawLevels'][i],
              dold['NewLevels'][i]))

    print()
    print('all new - old')
    for i in new_minus_old:
        print('  {}: [navalues {}] [rawlevels {}] [newlevels {}]'.format(
              i,
              dnew['NAValues'][i],
              dnew['RawLevels'][i],
              dnew['NewLevels'][i]))

    print()
    print('Intersection differences')
    for i in old_and_new:
        rold = dold.loc[i, :]
        rnew = dnew.loc[i, :]

        changed = []

        for col in rold.index:
            if col == 'Description':
                continue
            if pd.isna(rold[col]) and pd.isna(rnew[col]):
                continue
            elif rold[col] != rnew[col]:
                changed.append(col)

        if len(changed) > 0:
            print('  {}: {}'.format(
                i,
                ' '.join(['[{}: {} -> {}]'.format(
                    c, rold[c], rnew[c]) for c in changed])))


def main(args=None):

    print('WARNING: compare_tables.py is deprecated and will be removed in a '
          'future version of ukbparse. Variable and datacoding information '
          'is now stored in the ukbparse/data/field.txt and ukbparse/data/'
          'encoding.txt files. Updated copies of these files can be obtained '
          'from https://biobank.ctsu.ox.ac.uk/crystal/schema.cgi')
    print()


    if args is None:
        args = sys.argv[1:]

    if len(args) != 2:
        print('usage: compare_tables.py oldfile newfile')
        print()
        print(__doc__)
        sys.exit(0)

    oldfile, newfile = args

    compare(oldfile, newfile)


if __name__ == '__main__':
    main()
