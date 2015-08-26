#!/bin/bash

# Requires trackhub and bedfiles set

make -f Makefile.hub HUBROOT=/trackhub
make -f Makefile.bigwig HUBROOT=/trackhub BEDFILES_DIR=/data/central20bp FILE_PREFIX=E2F1
