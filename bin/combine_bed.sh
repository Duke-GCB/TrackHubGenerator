#!/bin/bash

# Extracts lines from input files beginning with chr
# Translates spaces to tabs
grep -h ^chr "$@" | tr ' ' '\t'
