FROM outlierbio/ob-pipelines

MAINTAINER Jake Feala <jake@outlierbio.com>

ARG SAMTOOLS_VERSION=1.3

ENV SCRATCH_DIR='/scratch'


# Install samtools
ADD https://github.com/samtools/samtools/releases/download/${SAMTOOLS_VERSION}/samtools-${SAMTOOLS_VERSION}.tar.bz2 /

RUN set -x && \
    yum install -y ncurses ncurses-devel && \
    tar -xvjf samtools-${SAMTOOLS_VERSION}.tar.bz2 && \
	cd /samtools-${SAMTOOLS_VERSION} && \
	make && \
	chmod 777 /samtools-${SAMTOOLS_VERSION}/samtools && \
	mv /samtools-${SAMTOOLS_VERSION}/samtools /usr/local/bin/ && \
	yum clean all && \
    yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    yum update -y && yum install -y python-wheel && yum install -y python-pip python-wheel && \
    pip install awscli

ADD *.sh /
