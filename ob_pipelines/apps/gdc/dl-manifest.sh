#!/usr/bin/env bash

DOWNLOAD_ID=$1
MANIFEST=$2
S3_OUTPATH=$3
TOKEN=$4

LOCAL_FOLDER=$SCRATCH/$DOWNLOAD_ID

mkdir -p $LOCAL_FOLDER

aws s3 cp $MANIFEST $LOCAL_FOLDER/manifest.txt
cd $SCRATCH

if [[ $TOKEN = *[!\ ]* ]]; then
  aws s3 cp $TOKEN $LOCAL_FOLDER/token.txt
  gdc-client download -m $LOCAL_FOLDER/manifest.txt -t $LOCAL_FOLDER/token.txt
  aws s3 cp $LOCAL_FOLDER $S3_OUTPATH --recursive --exlcude "token.txt" --exlcude="manifest.txt"
else
  gdc-client download -m $LOCAL_FOLDER/manifest.txt
  aws s3 cp $LOCAL_FOLDER $S3_OUTPATH --recursive --exlcude "token.txt" --exlcude="manifest.txt"
fi