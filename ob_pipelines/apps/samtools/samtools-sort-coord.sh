#!/usr/bin/env bash

INPUT=$1
OUTPUT=$2
TMP_PREFIX=$3

I_FILENAME=$(basename $INPUT)
O_FILENAME=$(basename $OUTPUT)
TMP_DIR=$TMP_PREFIX
INPUT_LOCAL=$INPUT

#Check if input file on S3, if yes - then copy to temporary dir
if [[ $INPUT == s3://* ]];
then
    mkdir -p $TMP_DIR
    aws s3 cp $INPUT $TMP_DIR/$I_FILENAME
    INPUT_LOCAL=$TMP_DIR/$I_FILENAME
fi

#output to local folder if $OUTPUT path is not on S3
OUTPUT_LOCAL=$OUTPUT
if [[ $OUTPUT == s3://* ]];
then
    OUTPUT_LOCAL=$TMP_DIR/$O_FILENAME
fi


samtools sort -m 8G -o $OUTPUT_LOCAL -T $TMP_PREFIX -@ 4 $INPUT_LOCAL

#Copy a resulted file to S3 if it is needed
if [[ $OUTPUT == s3://* ]];
then
    aws s3 cp $OUTPUT_LOCAL $OUTPUT
fi