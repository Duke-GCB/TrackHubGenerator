#!/bin/bash
set -e
JSON_DIR=$1
CWL_PATH=`pwd`/cwl/bin # Must be absolute
OUTDIR=$2
for f in $JSON_DIR/*.json; do
  PATH=$PATH:$CWL_PATH cwltool --outdir $OUTDIR cwl/bigbed-workflow.cwl $f
done
