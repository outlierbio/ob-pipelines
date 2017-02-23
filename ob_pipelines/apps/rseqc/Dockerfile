FROM python:2.7

# Install R
RUN apt-get update && apt-get -y install \
	r-base \
	r-base-core \
	r-recommended

# AWS
RUN pip install \
	awscli \
	boto3


# Install RSeQC
RUN pip install RSeQC
ADD hg38.HouseKeepingGenes.bed /hg38.housekeeping.bed
ADD hg19.HouseKeepingGenes.bed /hg19.housekeeping.bed

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch
VOLUME ["/reference"]
ENV REFERENCE_DIR=/reference

# ob-pipelines for common utils including s3wrap
RUN pip install git+https://github.com/outlierbio/ob-pipelines

ENTRYPOINT ["s3wrap"]