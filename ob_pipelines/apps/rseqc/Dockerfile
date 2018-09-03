FROM python:2.7

MAINTAINER Jake Feala <jake@outlierbio.com>

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch
VOLUME ["/reference"]
ENV REFERENCE_DIR=/reference

RUN set -x && \
    # Install R
    apt-get -qqy update && apt-get -qqy install r-base r-base-core r-recommended liblzo2-dev && \
    # AWS
    pip install awscli boto3 click numpy && \
    # Install RSeQC
    pip install RSeQC && \
    # ob-pipelines for common utils including s3wrap
    pip install git+https://github.com/outlierbio/ob-pipelines.git && \
	apt-get -qqy autoremove && apt-get -qqy clean
	
ADD rseqc.py /
ADD ./read_distribution.sh /
