#!/bin/bash

# Extracts lines from input files beginning with chr
# Sorts them by chrom then starting base
# Translates spaces to tabs
grep -h ^chr "$@" | sort -k1,1 -k2,2n | tr ' ' '\t'
