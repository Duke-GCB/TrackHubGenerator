#!/bin/bash

# Requires trackhub and bedfiles set

make -f Makefile.hub HUBROOT=/trackhub
make -f Makefile.bigwig HUBROOT=/trackhub BEDFILES_DIR=/data/central20bp/E2F1 FILE_PREFIX=E2F1
make -f Makefile.bigwig HUBROOT=/trackhub BEDFILES_DIR=/data/central20bp/E2F4 FILE_PREFIX=E2F4
