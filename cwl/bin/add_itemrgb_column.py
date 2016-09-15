#!/usr/bin/env python

from trackhub_utils import *
import sys
import argparse
import csv

RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255, 255, 255)
DEFAULT_SCORE = '0'
DEFAULT_STRAND = '+'

def extreme_scores(input, source_index=COL_VALUE):
    """
    Returns the minimum negative and maximum positive scores
    """
    reader = csv.reader(input, delimiter='\t')
    min_score, max_score = 0.0, 0.0
    for row in reader:
        score = float(row[source_index])
        if score < 0.0:
            min_score = min(min_score, score)
        elif score > 0.0:
            max_score = max(max_score, float(row[source_index]))
    return (min_score, max_score)

def scale_rgb(base_tuple, scale):
    # The base tuple will be something like (255,0,0) and then multipled by the scale
    return tuple([int(x * scale) for x in base_tuple])

def add_intermediate_columns(row, start_index=COL_START):
    # Row should have
    # 0. chrom
    # 1. chromStart
    # 2. chromEnd
    # 3. name
    # Need to add score, strand, thickStart, thickEnd
    row.append(DEFAULT_SCORE)
    row.append(DEFAULT_STRAND)
    # When there is no thick part, thickStart and thickEnd are usually set to the chromStart position.
    row.append(row[start_index])
    row.append(row[start_index])

def add_itemrgb_column(row, min_neg, max_pos, source_index=COL_VALUE):
    raw_value = float(row[source_index])
    if raw_value < 0.0:
        base_tuple = RED
        scale = raw_value / min_neg
    else:
        base_tuple = BLUE
        scale = raw_value / max_pos
    scaled_rgb = scale_rgb(base_tuple, scale)
    output_rgb = ','.join([str(x) for x in scaled_rgb])
    row.append(output_rgb)

def main(input, output):
    """
    Adds columns to a bed file for itemRGB
    :param input: An input stream or open file
    :param output: An output stream
    :param source_index: Column index containing the source value
    :return:
    """
    # First, get the minimum and maximum values
    min_neg, max_pos = extreme_scores(input)
    # Second, determine positive and negative scale
    input.seek(0)
    reader = csv.reader(input, delimiter='\t')
    writer = csv.writer(output, delimiter='\t')
    for row in reader:
        add_intermediate_columns(row)
        add_itemrgb_column(row, min_neg, max_pos)
        writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Resize ranges in a BED file')
    parser.add_argument('inputfile', type=argparse.FileType('rb'))
    args = parser.parse_args()
    main(args.inputfile, sys.stdout)
