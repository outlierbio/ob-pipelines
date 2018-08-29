#!/usr/bin/env bash

SOURCE=$1
DESTINATION=$REFERENCE_DIR
if ! [ -z "$2" ]; then
    DESTINATION=$2
fi

#downloading s3 objects from the bucket
aws s3 sync $SOURCE $DESTINATION