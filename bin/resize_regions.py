#!/usr/bin/env python
#
# resize_ranges
# Resizes ranges in a  BED file around a center point
#

import sys
import argparse
import csv

def resize_row(row, width):
    start, end = int(row[1]), int(row[2])
    original_range = end-start
    margin = (original_range - width) / 2
    start = start + margin
    end = end - margin
    row[1] = start
    row[2] = end
    return row

def resize_ranges(input, output, width):
    """
    Resizes regions in a bed file to the given width
    :param input: An input stream or open file
    :param output: An output stream
    :param width: the desired width
    :return:
    """
    reader = csv.reader(input, delimiter='\t')
    writer = csv.writer(output, delimiter='\t')
    for row in reader:
        writer.writerow(resize_row(row, width))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Resize ranges in a BED file')
    parser.add_argument('inputfile', type=argparse.FileType('rb'))
    parser.add_argument('width', type=int)
    parser.add_argument_group()
    args = parser.parse_args()
    resize_ranges(args.inputfile, sys.stdout, args.width)

