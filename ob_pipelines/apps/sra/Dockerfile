FROM centos:latest

MAINTAINER Jake Feala <jake@outlierbio.com>

ARG MINICONDA_VERSION=latest
ARG SRA_VERSION=current

VOLUME /scratch

RUN set -x && \
    yum update -y && \
    yum install -y bzip2 wget && \
    # Miniconda
    echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

ENV PATH /opt/conda/bin:$PATH

# NCBI SRA toolkit
WORKDIR /opt

RUN wget --quiet https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/${SRA_VERSION}/sratoolkit.${SRA_VERSION}-centos_linux64.tar.gz && \
	tar -xvf sratoolkit.${SRA_VERSION}-centos_linux64.tar.gz && \
	mv sratoolkit.${SRA_VERSION}-centos_linux64 sratoolkit

ENV PATH /opt/sratoolkit/bin:$PATH

## Controlled access data only
# Add project credentials to sratoolkit, then point download dir to /scratch
# ADD secrets/* /opt/sratoolkit/
# RUN for f in $(ls /opt/sratoolkit/prj_*.ngc ); \
#	do \
#		vdb-config --import $f; \
#		prj=$(basename $f .ngc | sed 's/prj_//'); \
#		vdb-config --root --set repository/user/protected/dbGaP-$prj/root=/scratch; \
#	done

# parallel-fastq-dump to parallelize downloads
RUN set -x && \
    conda install -c bioconda parallel-fastq-dump && \
    pip install awscli

ADD run.sh /
ENTRYPOINT ["sh", "/run.sh"]