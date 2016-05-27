#!/bin/bash
set -e
JSON_DIR=$1
CWL_PATH=`pwd`/cwl/bin # Must be absolute
OUTDIR=$2
for f in $JSON_DIR/*.json; do
  mkdir -p $OUTDIR/tmp
  TMPDIR=$OUTDIR/tmp PATH=$PATH:$CWL_PATH cwltool --preserve-environment PATH TMPDIR --outdir $OUTDIR cwl/bigbed-workflow-no-resize.cwl $f
  rm -r $OUTDIR/tmp
done
