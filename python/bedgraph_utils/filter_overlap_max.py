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


def process_region(region):
    # TODO: run max value in here
    return region


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
        maximized = process_region(overlap_region)
        for each in maximized:
            writer.writerow(each)
    last_region = process_region(queue)
    for each in last_region:
        writer.writerow(each)


if __name__ == '__main__':
    filter_overlap_max(fileinput.input(mode='rb'), sys.stdout)
