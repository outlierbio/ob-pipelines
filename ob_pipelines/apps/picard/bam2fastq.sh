#!/usr/bin/env bash

BAM=$1
OUT1=$2
OUT2=$3

BAMFILE=$(basename $BAM)
GZ1=$(basename $OUT1)
GZ2=$(basename $OUT2)
FQ1=${GZ1%.*}
FQ2=${GZ2%.*}

aws s3 cp $BAM $SCRATCH_DIR/$BAMFILE

java -jar /picard.jar \
	SamToFastq \
	I=$SCRATCH_DIR/$BAMFILE \
	FASTQ=$SCRATCH_DIR/$FQ1 \
	SECOND_END_FASTQ=$SCRATCH_DIR/$FQ2

gzip -c $SCRATCH_DIR/$FQ1 > $SCRATCH_DIR/$GZ1
gzip -c $SCRATCH_DIR/$FQ2 > $SCRATCH_DIR/$GZ2

aws s3 cp $SCRATCH_DIR/$GZ1 $OUT1
aws s3 cp $SCRATCH_DIR/$GZ2 $OUT2

rm $SCRATCH_DIR/$GZ1
rm $SCRATCH_DIR/$GZ2
rm $SCRATCH_DIR/$BAMFILE
