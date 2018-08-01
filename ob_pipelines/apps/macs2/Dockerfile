FROM python:2.7

MAINTAINER Jake Feala <jake@outlierbio.com>

RUN set -x && \
    pip install awscli boto3 click numpy pandas && \
    pip install MACS2

ENTRYPOINT ["s3wrap", "macs2"]