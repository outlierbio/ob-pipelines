#!/usr/bin/env bash

UUIDS=$1
TOKEN=$2
LOCAL_FOLDER=$SCRATCH

mkdir -p $LOCAL_FOLDER

cd $SCRATCH

if [[ $TOKEN = *[!\ ]* ]]; then
  aws s3 cp $TOKEN $LOCAL_FOLDER/token.txt
  gdc-client download $UUIDS -t $LOCAL_FOLDER/token.txt
else
  gdc-client download $UUIDS
fi