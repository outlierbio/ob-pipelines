FROM outlierbio/ob-pipelines

RUN yum update -y && yum install -y \
	ghostscript \
	libxml2-devel \
	libxslt-devel \
	perl-Data-Dumper \
	perl-HTML-Parser \
	perl-HTML-Tree \
	perl-JSON \
	perl-XML-Parser \
	perl-XML-Simple \
	which \
	zlib-devel

# Install MEME
ADD http://meme-suite.org/meme-software/4.12.0/meme_4.12.0.tar.gz /
RUN tar zxf /meme_4.12.0.tar.gz && \
	cd /meme_4.12.0 && \
	./configure --prefix=/root/meme --with-url=http://meme-suite.org \
		--enable-build-libxml2 --enable-build-libxslt && \
	make && \
	make install
ENV PATH /root/meme/bin:$PATH

