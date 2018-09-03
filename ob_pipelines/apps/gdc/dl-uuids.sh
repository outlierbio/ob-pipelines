#!/usr/bin/env bash

DOWNLOAD_ID=$1
S3_OUTPATH=$2
UUIDS=$3

LOCAL_FOLDER=$SCRATCH/$DOWNLOAD_ID

mkdir -p $LOCAL_FOLDER

cd $LOCAL_FOLDER

gdc-client download $UUIDS
aws s3 cp $LOCAL_FOLDER $S3_OUTPATH --recursive