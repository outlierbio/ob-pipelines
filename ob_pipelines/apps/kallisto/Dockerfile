FROM python:3.5
MAINTAINER Jake Feala <jake@outlierbio.com>

RUN pip install \
    awscli \
    boto3

RUN wget https://github.com/pachterlab/kallisto/releases/download/v0.43.0/kallisto_linux-v0.43.0.tar.gz && \
  tar -xvf kallisto_linux-v0.43.0.tar.gz && \
  cp kallisto_linux-v0.43.0/kallisto /usr/local/bin

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch
VOLUME ["/reference"]
ENV REFERENCE_DIR=/reference

RUN pip install git+https://github.com/outlierbio/ob-pipelines

ENTRYPOINT ["s3wrap", "kallisto"]