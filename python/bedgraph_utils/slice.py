from bedgraph_utils import *
import sys
import fileinput
import csv


def change_bedgraph_range(input, output, width=1):
    """
    Modifies bedgraph data so that end = start + width
    :param input: An input stream or open file
    :param output: An output stream
    :param width: Value to add to start to generate end
    :return:
    """
    reader = csv.reader(input, delimiter='\t')
    writer = csv.writer(output, delimiter='\t')
    for row in reader:
        start = int(row[COL_START])
        new_end = start + width
        row[COL_END] = str(new_end)
        writer.writerow(row)

if __name__ == '__main__':
    change_bedgraph_range(fileinput.input(mode='rb'), sys.stdout)
