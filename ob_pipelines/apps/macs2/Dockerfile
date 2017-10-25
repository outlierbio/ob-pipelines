FROM python:2.7
MAINTAINER Jake Feala <jake@outlierbio.com>

RUN pip install awscli boto3 click numpy pandas

RUN pip install MACS2

RUN pip install git+https://github.com/outlierbio/ob-pipelines

ENTRYPOINT ["s3wrap", "macs2"]