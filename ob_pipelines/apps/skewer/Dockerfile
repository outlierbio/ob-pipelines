FROM outlierbio/ob-pipelines

MAINTAINER Jake Feala <jake@outlierbio.com>

ARG SKEWER_VERSION=0.2.2

RUN set -x && \
    wget -O skewer https://sourceforge.net/projects/skewer/files/Binaries/skewer-${SKEWER_VERSION}-linux-x86_64/download && \
 	chmod 555 skewer && \
 	mv skewer /usr/local/bin

ENTRYPOINT ["s3wrap", "skewer"]