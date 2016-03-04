from bedgraph_utils import *
import sys
import fileinput
import csv


def add_column(input, output, source_index=BED_COL_NAME, factor=1000.0):
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
        row.append(float(row[BED_COL_NAME]) * factor)
        writer.writerow(row)

if __name__ == '__main__':
    add_column(fileinput.input(mode='rb'), sys.stdout)
