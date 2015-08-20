#!/bin/bash

# Sorts lines by chrom then starting base
# Uses -u to only return uniq starts, thus preventing overlaps

sort -u -k1,1 -k2,2n  "$@"
