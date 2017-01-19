FROM centos:7.0.1406
MAINTAINER Jake Feala <jake@outlierbio.com>

# yum packages
RUN yum install -y \
	bzip2 \
	gcc \
	gcc-c++ \
	make \
	python-devel \
	tar \
	wget

# pip packages
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py" && \
    python get-pip.py 
RUN pip install --upgrade pip && pip install \
	awscli \
	boto3 \
	click \
	ipython \
	luigi

# Install this package
RUN pip install git+https://github.com/outlierbio/ob-pipelines

ENTRYPOINT s3wrap