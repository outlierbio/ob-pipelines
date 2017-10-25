FROM python:2.7

# Install R
RUN apt-get update && apt-get -y install \
	r-base \
	r-base-core \
	r-recommended

# AWS
RUN pip install \
	awscli \
	boto3 \
	click

# Install RSeQC
RUN pip install RSeQC

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch
VOLUME ["/reference"]
ENV REFERENCE_DIR=/reference

# ob-pipelines for common utils including s3wrap
RUN pip install git+https://github.com/outlierbio/ob-pipelines.git

ADD rseqc.py /
ADD ./read_distribution.sh /
