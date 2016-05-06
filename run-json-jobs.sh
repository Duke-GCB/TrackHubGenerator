#!/bin/bash
set -e
JSON_DIR=$1
CWL_PATH=`pwd`/cwl/bin # Must be absolute

for f in $JSON_DIR/*.json; do
  PATH=$PATH:$CWL_PATH cwltool cwl/bigbed-workflow.cwl $f
  exit
done
