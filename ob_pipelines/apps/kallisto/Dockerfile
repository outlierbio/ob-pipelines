FROM python:3.5

MAINTAINER Jake Feala <jake@outlierbio.com>

ARG KALISTO_VERSION=0.43.0

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch
VOLUME ["/reference"]
ENV REFERENCE_DIR=/reference

RUN set -x && \
    pip install awscli boto3 git+https://github.com/outlierbio/ob-pipelines && \
    wget https://github.com/pachterlab/kallisto/releases/download/v${KALISTO_VERSION}/kallisto_linux-v${KALISTO_VERSION}.tar.gz && \
    tar -xvf kallisto_linux-v${KALISTO_VERSION}.tar.gz && \
    cp kallisto_linux-v${KALISTO_VERSION}/kallisto /usr/local/bin

ENTRYPOINT ["s3wrap", "kallisto"]