FROM outlierbio/samtools

MAINTAINER Jake Feala <jake@outlierbio.com>

# Volumes and scratch drive for reference data
VOLUME ["/reference"]
VOLUME ["/scratch"]
ENV REFERENCE_DIR /reference
ENV SCRATCH_DIR /scratch

RUN set -x && \
    git clone https://github.com/lh3/bwa.git && \
	cd bwa && \
	make
ENV PATH $PATH:/bwa

ADD ./bwa.py /src/

ENTRYPOINT ["python", "/src/bwa.py"]
	