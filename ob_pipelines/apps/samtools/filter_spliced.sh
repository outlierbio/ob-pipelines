#!/usr/bin/env bash

IN=$1
OUT=$2

IN_LOCAL=$SCRATCH_DIR/$(basename $IN)
OUT_LOCAL=$SCRATCH_DIR/$(basename $OUT)

aws s3 cp $IN $IN_LOCAL

samtools view -H $IN_LOCAL > $SCRATCH_DIR/header.txt
samtools view $IN_LOCAL | awk '($6 ~ /N/)' > $SCRATCH_DIR/filtered.sam
cat $SCRATCH_DIR/header.txt $SCRATCH_DIR/filtered.sam | samtools view -bS > $OUT_LOCAL

aws s3 cp $OUT_LOCAL $OUT