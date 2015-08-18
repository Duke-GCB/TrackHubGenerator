#!/bin/bash

# bedGraphToBigWig requires columns with 4 fields:
#       <chrom> <start> <end> <value>

awk '{print $1 "\t" $2 "\t" $3 "\t" $5}' $@

