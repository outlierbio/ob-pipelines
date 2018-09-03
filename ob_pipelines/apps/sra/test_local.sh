<<<<<<< HEAD
=======
#!/usr/bin/env bash

>>>>>>> 8ad2da5ddc9fbfad9056230d696b6eada3ef039c
SCRATCH_DIR=~/Desktop/scratch

image=outlierbio/sra
docker build -t $image .
docker run --rm \
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    -v $SCRATCH_DIR:/scratch \
    $image SRR1024804 paired s3://vl46-ngs-raw/test/

$(aws ecr get-login --no-include-email)
docker push $image