from trackhub_utils import *
import sys
import fileinput
import csv
import math

MAX_INTENSITY = 255.0

def score_to_rgb(score):
    """
    :param score: A score, between 0.0 and 1.0
    :return: a string, indicating an rgb color value
    """
    # 0.0 -> white
    # 1.0 -> black
    # High scores should be darker black, which are lower intensiies
    intensity = int(math.floor((MAX_INTENSITY - (float(score) * MAX_INTENSITY))))
    return '{},{},{}'.format(intensity, intensity, intensity)


def add_score_and_rgb_columns(input, output, source_index=BED_COL_NAME, factor=1000.0):
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
        # Expands a row with CHROM, START, STOP, SCORE to BED with fields up to itemRgb
        # http://genome.ucsc.edu/FAQ/FAQformat.html#format1
        # score
        row.append(int(float(row[BED_COL_NAME]) * factor))
        # strand
        row.append('+')
        # thickStart, thickEnd
        # When there is no thick part, thickStart and thickEnd are usually set to the chromStart position.
        row.append(row[COL_START])
        row.append(row[COL_START])
        # itemRGB
        row.append(score_to_rgb(row[BED_COL_NAME]))
        writer.writerow(row)

if __name__ == '__main__':
    add_score_and_rgb_columns(fileinput.input(mode='rb'), sys.stdout)
