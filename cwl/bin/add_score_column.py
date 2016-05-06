#!/usr/bin/env python

from trackhub_utils import *
import sys
import fileinput
import csv


def add_score_column(input, output, source_index=COL_VALUE, factor=1000.0):
    """
    Adds a score column to a bed file by multiplying the
    value of one column by a factor
    :param input: An input stream or open file
    :param output: An output stream
    :param source_index: Column index containing the source value
    :param factor: Value by which to multiply
    :return:
    """
    reader = csv.reader(input, delimiter='\t')
    writer = csv.writer(output, delimiter='\t')
    for row in reader:
        # Adds a score column by multiplying the value of an existing column by a factor
        # http://genome.ucsc.edu/FAQ/FAQformat.html#format1
        row.append(int(min(float(row[source_index]) * factor, factor)))
        writer.writerow(row)

if __name__ == '__main__':
    add_score_column(fileinput.input(mode='rb'), sys.stdout)
