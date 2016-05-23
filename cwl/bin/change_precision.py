#!/usr/bin/env python

from trackhub_utils import *
import sys
import argparse
import csv


def change_precision(input, output, precision, source_index=COL_VALUE):
    """
    Changes the precision of the value at source_index to precision
    value of one column by a factor
    :param input: An input stream or open file
    :param output: An output stream
    :param precision: Number of decimal places to use
    :param source_index: Column index containing the source value
    :return: None
    """
    reader = csv.reader(input, delimiter='\t')
    writer = csv.writer(output, delimiter='\t')
    for row in reader:
        orig_prediction = float(row[source_index])
        row[source_index] = '{:.{prec}f}'.format(orig_prediction, prec=precision)
        writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Change precision of a float column in a BED file')
    parser.add_argument('inputfile', type=argparse.FileType('rb'))
    parser.add_argument('precision', type=int)
    parser.add_argument_group()
    args = parser.parse_args()
    change_precision(args.inputfile, sys.stdout, args.precision)
