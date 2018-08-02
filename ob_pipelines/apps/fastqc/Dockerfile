FROM openjdk:8

MAINTAINER Jake Feala <jake@outlierbio.com>

ARG FASTQC_VERSION=0.11.5

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch

RUN set -x && \
    apt-get update && apt-get install -y python-pip && \
    pip install boto3 click && \
    # Install FastQC
    wget -q http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v${FASTQC_VERSION}.zip -O /fastqc_v${FASTQC_VERSION}.zip && \
	unzip /fastqc_v${FASTQC_VERSION}.zip && \
	chmod 777 /FastQC/fastqc && \
	pip install git+https://github.com/outlierbio/ob-pipelines && \
	apt-get -qqy autoremove && apt-get -qqy clean

ENV PATH /FastQC:$PATH

ADD fastqc.py /

ENTRYPOINT ["python", "/fastqc.py"]
