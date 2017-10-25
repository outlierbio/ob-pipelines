FROM openjdk:8

RUN apt-get update && apt-get install -y python-pip
RUN pip install awscli boto3

# Install Picard
ADD https://github.com/broadinstitute/picard/releases/download/2.8.3/picard.jar /

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch

RUN pip install git+https://github.com/outlierbio/ob-pipelines

ADD ./bam2fastq.sh /