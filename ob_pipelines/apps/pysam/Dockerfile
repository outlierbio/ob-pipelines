FROM python:2.7
MAINTAINER Jake Feala <jake@outlierbio.com>

# AWS
RUN pip install \
	awscli \
	boto3 \
	click \
	pysam

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch

RUN pip install git+https://github.com/outlierbio/ob-pipelines

ADD ./dedupe.py /src/

