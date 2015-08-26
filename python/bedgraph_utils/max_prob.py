#!/usr/bin/env python

COL_CHROM = 0
COL_START = 1
COL_END = 2
COL_VALUE = 3

ranges = [
    ('chr1', 1, 3, 0.9),
    ('chr1', 2, 4, 0.95),
    ('chr1', 5, 7, 0.75),
    ('chr1', 10, 12, 0.05)
]


class MaxProb(object):
    def __init__(self, ranges):
        self.ranges = ranges
        self.rows = []

    def add_row(self, row):
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
            self.flush(overlaps)

    def rows_covering_base(self, rows, base):
        cover = []
        for row in rows:
            if row[COL_START] <= base < row[COL_END]:
                cover.append(row)
        return cover

    def flush(self, rows):
        chrom = rows[0][COL_CHROM]
        start = min([x[COL_START] for x in rows])
        end = max([x[COL_END] for x in rows])
        for base in range(start, end):
            overlap_rows = self.rows_covering_base(rows, base)
            value = max([x[COL_VALUE] for x in overlap_rows])
            print chrom, base, base + 1, value

    def max_prob(self):
        for row in self.ranges:
            self.add_row(row)
        self.flush(self.rows)


m = MaxProb(ranges)
m.max_prob()
