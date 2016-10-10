#!/usr/bin/env python

from trackhub_utils import *
import sys
import argparse
import csv
import pandas

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

# midnightblue is the darkest, should be associated with the most extreme value,
# and therefore be first.
BLUES = (
    (25, 25, 112),    # midnightblue
    (54, 100, 139),   # steelblue4
    (70, 130, 180),   # steelblue
    (79, 148, 205),   # steelblue3
    (92, 172, 238),   # steelblue2
    (99, 184, 255),   # steelblue1
)

DEFAULT_SCORE = '0'
DEFAULT_STRAND = '+'

def label_from_rgb_tuple(rgb_tuple):
    return ','.join([str(c) for c in rgb_tuple])

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

def main(input, output):
    """
    Adds columns to a bed file for itemRGB
    :param input: An input stream or open file
    :param output: An output stream
    :param source_index: Column index containing the source value
    :return:
    """
    pos_labels = [label_from_rgb_tuple(t) for t in REDS]
    neg_labels = [label_from_rgb_tuple(t) for t in BLUES]
    names = ['chrom','start','end','pref']
    data = pandas.read_table(input, names=names, delimiter=' ')
    # Assign color labels based on quantile cutting
    data.loc[data['pref'] == 0, 'label'] = label_from_rgb_tuple(GRAY)
    data.loc[data['pref'] > 0, 'label'] = pandas.qcut(data[data['pref'] > 0]['pref'], len(pos_labels), labels=pos_labels)
    data.loc[data['pref'] < 0, 'label'] = pandas.qcut(data[data['pref'] < 0]['pref'], len(neg_labels), labels=neg_labels)
    writer = csv.writer(output, delimiter='\t')
    for idx, input_row in data.iterrows():
        row = [input_row[name] for name in names]
        add_intermediate_columns(row)
        row.append(input_row['label'])
        writer.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Resize ranges in a BED file')
    parser.add_argument('inputfile', type=argparse.FileType('rb'))
    args = parser.parse_args()
    main(args.inputfile, sys.stdout)
