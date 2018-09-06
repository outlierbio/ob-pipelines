#!/usr/bin/env bash

SCRATCH_DIR=~/Desktop/scratch
TEST_BUCKET=

image=outlierbio/sra
docker build -t $image .
docker run --rm \
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    -v $SCRATCH_DIR:/scratch \
    $image SRR1024804 paired s3://$TEST_BUCKET/test/

$(aws ecr get-login --no-include-email)
docker push $image