#!/usr/bin/env python

import sys
import argparse
import csv


def remove_zeroes(input, output, source_index=3):
    """
    Filters a predictions bed file by returning only rows where the score is
    nonzero
    :param input: An input stream or open file
    :param output: An output stream
    :param source_index: Column index containing the source value
    :return:
    """
    reader = csv.reader(input, delimiter='\t')
    writer = csv.writer(output, delimiter='\t')
    for row in reader:
        if float(row[source_index]) != 0.0:
            writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', type=argparse.FileType('rb'))
    parser.add_argument_group()
    args = parser.parse_args()
    remove_zeroes(args.inputfile, sys.stdout)
