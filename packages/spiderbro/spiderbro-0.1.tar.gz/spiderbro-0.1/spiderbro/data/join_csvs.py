#! /usr/bin/env python3
"""
Copyright: GPLv3 <Bernardas Ališauskas @ bernardas.alisauskas@pm.me>

join-csvs: Join multiple csvs into one combined csv by specific column

Requires:
    python3.6+
    click

Arguments:
    id - which is column name for determining which rows should be combined
    outfile - combined output filepath
    infiles - files that should be combined

Usage:
    data between is update in provided file order:

        $ join-csvs id combined.csv file1.csv file2.csv

        # file1.csv
        id,b,c,d
        1,2,3,9
        # file2.csv
        id,b,c,e
        1,5,3,7
        ==============
        # combined.csv
        id,b,c,d,e
        1,5,3,9,7

Options:
    --append - append some columns instead of updating:

        $ join-csvs id combined.csv file1.csv file2.csv --append c

        # file1.csv
        id,b,c
        1,2,3
        # file2.csv
        id,b,c
        1,5,5
        ==============
        # combined.csv
        id,b,c_file1,c_file2
        1,5,3,5
"""
import csv
from collections import defaultdict
from pathlib import Path

import click


@click.command()
@click.argument('id')
@click.argument('outfile', type=click.File('w'))
@click.argument('infiles', type=click.File('r'), nargs=-1)
@click.option('--append', help='comma separated fields to append to current set')
def main(id, infiles, append, outfile):
    """
    Join multiple csvs by specific column updating values in input file order
    """
    append = append.split(',') if append else []
    data = defaultdict(list)

    for file in infiles:
        reader = csv.DictReader(file)
        for row in reader:
            row['file'] = Path(file.name).name.split('.')[0]
            data[row[id]].append(row)
    combined = defaultdict(dict)
    for key, values in data.items():
        for v in values:
            combined[key].update(v)
            for a in append:
                combined[key][f'{a}_{v["file"]}'] = v[a]
                combined[key].pop(a)

    # remove file meta column
    for value in combined.values():
        value.pop('file')

    # make headers and sort them
    # also ensure that appended headers go in the back
    # and that id is first column
    headers = set()
    appended_headers = set()
    for value in combined.values():
        for k in value:
            if any(k.startswith(a + '_') for a in append):
                appended_headers.add(k)
            else:
                headers.add(k)
    headers = [id] + [x for x in sorted(headers) + sorted(appended_headers) if x != id]

    # write output
    writer = csv.DictWriter(outfile, headers)
    writer.writeheader()
    for row in combined.values():
        writer.writerow(row)


if __name__ == '__main__':
    main()
