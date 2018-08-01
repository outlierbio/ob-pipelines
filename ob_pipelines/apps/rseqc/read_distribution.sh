#!/usr/bin/env bash

BAM=$1
BED=$2
OUT=$3

BAMFILE=$(basename $BAM)
OUTFILE=$(basename $OUT)

# TODO: also download BED if starts with s3://
aws s3 cp $BAM $SCRATCH_DIR/$BAMFILE

read_distribution.py -i $SCRATCH_DIR/$BAMFILE -r $BED > $SCRATCH_DIR/$OUTFILE

aws s3 cp $SCRATCH_DIR/$OUTFILE $OUT