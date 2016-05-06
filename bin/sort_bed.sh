#!/bin/bash

# Sorts lines by chrom then starting base

LC_COLLATE=C sort -k1,1 -k2,2n  "$@"
