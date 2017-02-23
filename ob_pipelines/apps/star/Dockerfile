FROM python:3.5
MAINTAINER Jake Feala <jake@outlierbio.com>

RUN pip install \
    awscli \
    boto3 \
    click

RUN wget https://github.com/alexdobin/STAR/releases/download/2.5.0b/Linux_x86_64_static_gcc.tgz && \
  tar -xvzf Linux_x86_64_static_gcc.tgz && \
  cp Linux_x86_64_static_gcc5.3.0/STAR /bin

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch
VOLUME ["/reference"]
ENV REFERENCE_DIR=/reference

RUN pip install git+https://github.com/outlierbio/ob-pipelines

ADD star.py /

ENTRYPOINT ["python", "/star.py"]
