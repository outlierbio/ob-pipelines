FROM python:2.7

MAINTAINER Jake Feala <jake@outlierbio.com>

RUN set -x && \
    pip install awscli boto3 click numpy pandas MACS2 git+https://github.com/outlierbio/ob-pipelines

ENTRYPOINT ["s3wrap", "macs2"]