FROM centos:7.0.1406
MAINTAINER Jake Feala <jake@outlierbio.com>

# yum packages
RUN yum install -y \
	bzip2 \
    bzip2-devel \
	ca-certificates \
	gcc \
	gcc-c++ \
	git \
	make \
    nano \
	python-devel \
	tar \
	wget

# Miniconda 3 (from continuumio/miniconda3)
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.1.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh
ENV PATH /opt/conda/bin:$PATH

# Conda packages
RUN conda install -y \
	boto3 \
	click \
	ipython

# Required for Click on Python3
ENV LC_ALL en_US.utf-8
ENV LANG en_US.utf-8

# pip packages
RUN pip install \
	awscli \
	luigi

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch

# Install or ADD this package
# RUN pip install git+https://github.com/outlierbio/ob-pipelines.git
ADD ./setup.py /src/
ADD ./test /src/test
ADD ./ob_pipelines/*.py /src/ob_pipelines/
RUN cd /src && pip install -e .