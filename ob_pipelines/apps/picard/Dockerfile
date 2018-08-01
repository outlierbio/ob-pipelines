FROM openjdk:8

MAINTAINER Jake Feala <jake@outlierbio.com>

ARG PICARD_VERSION=2.8.3

# Install Picard
ADD https://github.com/broadinstitute/picard/releases/download/${PICARD_VERSION}/picard.jar /

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch


RUN set -x && \
    apt-get update && apt-get install -y python-pip && \
    pip install awscli boto3 && \
    pip install git+https://github.com/outlierbio/ob-pipelines

ADD ./bam2fastq.sh /