#!/usr/bin/env python
import sys
import fileinput
import csv
from bedgraph_utils import *


def convert_row(row):
    return row[COL_CHROM], int(row[COL_START]), int(row[COL_END]), float(row[COL_VALUE])


def find_gap(queue):
    if len(queue) < 2:
        return None
    index = None
    chrom = queue[0][COL_CHROM]
    range_end = queue[0][COL_END]
    for i in range(1,len(queue)):
        if queue[i][COL_START] >= range_end or queue[i][COL_CHROM] != chrom:
            index = i
            break
    return index


def rows_covering_base(rows, base):
    for row in rows:
        if row[COL_START] <= base < row[COL_END]:
            yield row


def collapse_region(region):
    chrom, start, end, value = None, None, None, None
    for r in region:
        value = value or r[COL_VALUE]
        chrom = chrom or r[COL_CHROM]
        start = start or r[COL_START]
        end = end or r[COL_END]
        if value == r[COL_VALUE]:
            end = r[COL_END]
        else:
            # Clear out old region, begin new
            yield (chrom, start, end, value)
            # new value, new region
            value = r[COL_VALUE]
            start = r[COL_START]
            end = r[COL_END]
    yield (chrom, start, end, value)


def expand_region(region):
    chrom = region[0][COL_CHROM]
    start = min([x[COL_START] for x in region])
    end = max([x[COL_END] for x in region])
    for base in range(start, end):
        value = max([x[COL_VALUE] for x in rows_covering_base(region, base)])
        yield (chrom, base, base + 1, value)


def process_region(region):
    for c in collapse_region(expand_region(region)):
        yield c


def filter_overlap_max(input_file, output_file):
    """
    Examines regions in bedgraph data and returns maximum value of input for overlapping regions
    :param input_file: An input stream or open file
    :param output_file: An output stream
    :return:
    """
    reader = csv.reader(input_file, delimiter='\t')
    writer = csv.writer(output_file, delimiter='\t')
    queue = []
    for text_row in reader:
        row = convert_row(text_row)
        # Add the row to the queue
        queue.append(row)
        # Check, from the beginning of the queue if there is a gap
        gap_index = find_gap(queue)
        # if no gap, continue
        if gap_index is None:
            continue
        # if gap, process everything before the gap
        overlap_region = queue[:gap_index]
        queue = queue[gap_index:]
        for r in process_region(overlap_region):
            writer.writerow(r)
    # Flush the last region
    for r in process_region(queue):
        writer.writerow(r)


if __name__ == '__main__':
    filter_overlap_max(fileinput.input(mode='rb'), sys.stdout)
