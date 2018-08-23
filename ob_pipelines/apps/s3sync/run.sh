#!/usr/bin/env bash

S3_BUCKET=$1

#downloading s3 objects from the bucket
aws s3 sync $S3_BUCKET $REFERENCE_DIR