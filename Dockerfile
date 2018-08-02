FROM centos:7.4.1708

MAINTAINER Jake Feala <jake@outlierbio.com>

ARG MINICONDA_VERSION=latest

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch

# Required for Click on Python3
ENV LC_ALL en_US.utf-8
ENV LANG en_US.utf-8

# yum packages
RUN set -x && \
    yum -y update && yum install -y bzip2 bzip2-devel ca-certificates gcc gcc-c++ git make \
    nano python-devel python-setuptools python-setuptools-devel tar wget zlib-devel && \
    easy_install pip  && \
    # pip packages
    pip install awscli luigi && \
    pip install git+https://github.com/outlierbio/ob-pipelines.git && \
    # Miniconda 3 (from continuumio/miniconda3)
    echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
	yum clean all

ENV PATH /opt/conda/bin:$PATH

RUN set -x && \
    # Conda packages
    conda install -y nomkl && \
    conda install -y boto3 click ipython

