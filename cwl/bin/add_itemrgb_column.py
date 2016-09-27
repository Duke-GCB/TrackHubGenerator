#!/usr/bin/env python

from trackhub_utils import *
import sys
import argparse
import csv
from color import polylinear_gradient, RGB_to_hex, color_dict

# Color constant for Gray
GRAY = (190, 190, 190)

# Color constants for Red gradient
# From Colorbrewer Red 9 http://colorbrewer2.org/?type=sequential&scheme=Reds&n=9
REDS = (
    (255, 245, 240),
    (254, 224, 210),
    (252, 187, 161),
    (252, 146, 114),
    (251, 106, 74),
    (239, 59, 44),
    (203, 24, 29),
    (165, 15, 21),
    (103, 0, 13),
)

# Color constants for blue gradient
# Converted to RGB from R Color names
# plotclr2 = c("midnightblue","steelblue4","steelblue","steelblue3","steelblue2","steelblue1")
# using chart at http://research.stowers-institute.org/efg/R/Color/Chart/ColorChart.pdf

# midnightblue is the darkest, should be associated with the highest value,
# and therefore be last.
BLUES = (
    (99, 184, 255),   # steelblue1
    (92, 172, 238),   # steelblue2
    (79, 148, 205),   # steelblue3
    (70, 130, 180),   # steelblue
    (54, 100, 139),   # steelblue4
    (25, 25, 112),    # midnightblue
)

GRADIENT_STEPS = 64
RED_GRADIENT = polylinear_gradient([RGB_to_hex(x) for x in REDS], GRADIENT_STEPS)
BLUE_GRADIENT = polylinear_gradient([RGB_to_hex(x) for x in BLUES], GRADIENT_STEPS)
GRAY_GRADIENT = color_dict([GRAY])
DEFAULT_SCORE = '0'
DEFAULT_STRAND = '+'
BLOCK_COUNT = '0'

def scale_color(factor, gradient):
    # Factor is 0.0 - 1.0
    entries = len(gradient['hex'])
    index = min(int(factor * entries), entries - 1)
    return dict([(d, gradient[d][index]) for d in ['b','r','hex','g']])

def color_to_string(color_dict):
    return ','.join([str(color_dict[d]) for d in ('r','g','b')])

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

def add_block_count_column(row):
    row.append(BLOCK_COUNT)

def add_itemrgb_column(row, min_neg, max_pos, source_index=COL_VALUE):
    raw_value = float(row[source_index])
    if raw_value < 0.0:
        gradient = BLUE_GRADIENT
        factor = raw_value / min_neg
    elif raw_value > 0.0:
        gradient = RED_GRADIENT
        factor = raw_value / max_pos
    else:
        gradient = GRAY_GRADIENT
        factor = 0.0
    scaled_color = scale_color(factor, gradient)
    output_rgb = color_to_string(scaled_color)
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
        add_block_count_column(row)
        writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Resize ranges in a BED file')
    parser.add_argument('inputfile', type=argparse.FileType('rb'))
    args = parser.parse_args()
    main(args.inputfile, sys.stdout)
