FROM python:3.5

MAINTAINER Jake Feala <jake@outlierbio.com>

ARG STAR_VERSION=2.5.0b

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch
VOLUME ["/reference"]
ENV REFERENCE_DIR=/reference

RUN set -x && \
    pip install awscli boto3 click && \
    wget -q https://github.com/alexdobin/STAR/releases/download/${STAR_VERSION}/Linux_x86_64_static_gcc.tgz && \
    tar -xvzf Linux_x86_64_static_gcc.tgz && \
    cp Linux_x86_64_static_gcc5.3.0/STAR /bin && \
    pip install git+https://github.com/outlierbio/ob-pipelines

ADD star.py /

ENTRYPOINT ["python", "/star.py"]
