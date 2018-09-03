FROM python:2.7

MAINTAINER Jake Feala <jake@outlierbio.com>

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch

# AWS
RUN set -x && \
    pip install awscli boto3 click pysam && \
    pip install git+https://github.com/outlierbio/ob-pipelines

ADD ./dedupe.py /src/

