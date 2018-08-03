FROM outlierbio/ob-pipelines

MAINTAINER Jake Feala <jake@outlierbio.com>

ARG MEME_VERSION=4.12.0

ADD http://meme-suite.org/meme-software/${MEME_VERSION}/meme_${MEME_VERSION}.tar.gz /

RUN set -x && \
    yum update -y && yum install -y ghostscript libxml2-devel libxslt-devel \
	perl-Data-Dumper perl-HTML-Parser perl-HTML-Tree perl-JSON \
	perl-XML-Parser perl-XML-Simple which zlib-devel && \
    # Install MEME
    tar zxf /meme_${MEME_VERSION}.tar.gz && \
	cd /meme_${MEME_VERSION} && \
	./configure --prefix=/root/meme --with-url=http://meme-suite.org \
		--enable-build-libxml2 --enable-build-libxslt && \
	make && \
	make install && \
	yum clean all

ENV PATH /root/meme/bin:$PATH

