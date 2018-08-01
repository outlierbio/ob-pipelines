FROM outlierbio/ob-pipelines

MAINTAINER Jake Feala <jake@outlierbio.com>

ARG SUBREAD_VERSION=1.5.3

RUN set -x && \
    wget -O subread-${SUBREAD_VERSION}-Linux-x86_64.tar.gz https://sourceforge.net/projects/subread/files/subread-${SUBREAD_VERSION}/subread-${SUBREAD_VERSION}-Linux-x86_64.tar.gz/download && \
    tar -xvf subread-${SUBREAD_VERSION}-Linux-x86_64.tar.gz

ENV PATH /subread-${SUBREAD_VERSION}-Linux-x86_64/bin:$PATH

ENTRYPOINT ["s3wrap", "featureCounts"]
