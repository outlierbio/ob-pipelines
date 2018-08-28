#!/usr/bin/env bash

S3_BUCKET=$1

#downloading s3 objects from the bucket
echo "AWS S3 SYNC"
echo "BUCKET: $S3_BUCKET"
echo "REFERENCE_DIR: $REFERENCE_DIR"
aws s3 sync $S3_BUCKET $REFERENCE_DIR
echo "AWS S3 SYNC COMPLETED $(exit $?)"