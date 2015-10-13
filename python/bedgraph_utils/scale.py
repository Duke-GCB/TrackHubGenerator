from bedgraph_utils import *
import sys
import fileinput
import csv


def change_bedgraph_score_scale(input, output, factor=.01):
    """
    Modifies bedgraph data by multiplying by a scale factor
    :param input: An input stream or open file
    :param output: An output stream
    :param factor: Value by which to multiply COL_VALUE
    :return:
    """
    reader = csv.reader(input, delimiter='\t')
    writer = csv.writer(output, delimiter='\t')
    for row in reader:
        row[COL_VALUE] = float(row[COL_VALUE]) * factor
        writer.writerow(row)

if __name__ == '__main__':
    change_bedgraph_score_scale(fileinput.input(mode='r'), sys.stdout)
