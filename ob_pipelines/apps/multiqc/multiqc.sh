#!/usr/bin/env bash

S3_FOLDER=$1
LOCAL_FOLDER=$SCRATCH/multiqc/$(dirname $S3_FOLDER)

mkdir -p $LOCAL_FOLDER
aws s3 sync $S3_FOLDER $LOCAL_FOLDER \
	--exclude="*.bam*" --exclude="*.fq*" --exclude="*.fastq*" \
	--exclude="*mate*" --exclude="abundance.*"

multiqc $LOCAL_FOLDER

aws s3 cp multiqc_report.html $S3_FOLDER
aws s3 cp multiqc_data/ $S3_FOLDER/multiqc_data/ --recursive