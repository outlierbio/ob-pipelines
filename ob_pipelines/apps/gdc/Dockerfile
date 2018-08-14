FROM centos:latest

MAINTAINER Alexander Salimonov <asalimonov@bekitzur.com>

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch

ARG GDC_VERSION=1.3.0

RUN set -x && \
    yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    yum update -y && yum install -y python-wheel && yum install -y python-pip python-wheel && \
    pip install awscli boto3 && \
    mkdir gdc-client && \
    cd /gdc-client && \
    yum update -y && yum install -y wget unzip && \
    wget -q https://gdc.cancer.gov/system/files/authenticated%20user/0/gdc-client_v${GDC_VERSION}_CentOS7_x64_Beta.zip -O gdc-client_v${GDC_VERSION}_CentOS7_x64_Beta.zip && \
    unzip gdc-client_v${GDC_VERSION}_CentOS7_x64_Beta.zip && rm gdc-client_v${GDC_VERSION}_CentOS7_x64_Beta.zip && \
    chmod 777 /gdc-client/gdc-client

ENV PATH /gdc-client:$PATH

ADD *.sh /

