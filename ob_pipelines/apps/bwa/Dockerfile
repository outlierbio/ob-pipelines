FROM outlierbio/samtools
MAINTAINER Jake Feala <jake@outlierbio.com>

RUN git clone https://github.com/lh3/bwa.git && \
	cd bwa && \
	make
ENV PATH $PATH:/bwa

# Volumes and scratch drive for reference data
VOLUME ["/reference"]
VOLUME ["/scratch"]
ENV REFERENCE_DIR /reference
ENV SCRATCH_DIR /scratch

ADD ./bwa.py /src/

ENTRYPOINT ["python", "/src/bwa.py"]
	