#!/usr/bin/env python
import sys
import fileinput
import csv
from bedgraph_utils import *


class OverlapMaxValue(object):
    def __init__(self, writer=None):
        self.rows = []
        self.writer = writer

    def push_row(self, row):
        self.rows.append(row)
        self.process_overlaps()

    def process_overlaps(self):
        if len(self.rows) < 2:
            return
        overlaps = []
        for i in range(len(self.rows) - 1):
            a = self.rows[i]
            b = self.rows[i + 1]
            a_end = a[COL_END]
            b_start = b[COL_START]
            if b_start > a_end:
                # flush overlaps
                overlaps = self.rows[:i+1]
                self.rows = self.rows[i+1:]
                break
        if len(overlaps) > 0:
            self.flush_rows(overlaps)

    @staticmethod
    def rows_covering_base(rows, base):
        cover = []
        for row in rows:
            if row[COL_START] <= base < row[COL_END]:
                cover.append(row)
        return cover

    def flush(self):
        self.flush_rows(self.rows)

    def flush_rows(self, rows):
        chrom = rows[0][COL_CHROM]
        start = min([x[COL_START] for x in rows])
        end = max([x[COL_END] for x in rows])
        for base in range(start, end):
            overlap_rows = self.rows_covering_base(rows, base)
            value = max([x[COL_VALUE] for x in overlap_rows])
            row = (chrom, base, base + 1, value)
            if self.writer is not None:
                self.writer.writerow(row)
            else:
                print row


def convert_row(row):
    return row[COL_CHROM], int(row[COL_START]), int(row[COL_END]), float(row[COL_VALUE])


def filter_overlap_max(input_file, output_file):
    """
    Examines regions in bedgraph data and returns maximum value of input for overlapping regions
    :param input_file: An input stream or open file
    :param output_file: An output stream
    :return:
    """
    reader = csv.reader(input_file, delimiter='\t')
    writer = csv.writer(output_file, delimiter='\t')
    overlap_max_value = OverlapMaxValue(writer)
    for text_row in reader:
        row = convert_row(text_row)
        overlap_max_value.push_row(row)
    overlap_max_value.flush()


if __name__ == '__main__':
    filter_overlap_max(fileinput.input(mode='rb'), sys.stdout)
