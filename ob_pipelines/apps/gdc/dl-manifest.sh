#!/usr/bin/env bash

MANIFEST=$1
TOKEN=$2
LOCAL_FOLDER=$SCRATCH/in

mkdir -p $LOCAL_FOLDER

aws s3 cp $MANIFEST $LOCAL_FOLDER/manifest.txt
cd $SCRATCH

if [[ $TOKEN = *[!\ ]* ]]; then
  aws s3 cp $TOKEN $LOCAL_FOLDER/token.txt
  gdc-client download -m $LOCAL_FOLDER/manifest.txt -t $LOCAL_FOLDER/token.txt
else
  gdc-client download -m $LOCAL_FOLDER/manifest.txt
fi