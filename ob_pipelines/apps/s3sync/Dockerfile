FROM centos:latest

MAINTAINER Alexander Salimonov <asalimonov@bekitzur.com>

VOLUME ["/reference"]
ENV REFERENCE_DIR=/reference

#https://docs.aws.amazon.com/cli/latest/userguide/installing.html
RUN set -x && \
    yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    yum update -y && yum install -y python-wheel && yum install -y python-pip python-wheel && \
    pip install awscli

ADD *.sh /

