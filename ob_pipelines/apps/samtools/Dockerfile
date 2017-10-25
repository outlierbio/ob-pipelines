FROM outlierbio/ob-pipelines

RUN yum install -y ncurses ncurses-devel

# Install samtools
ADD https://github.com/samtools/samtools/releases/download/1.3/samtools-1.3.tar.bz2 /
RUN tar -xvjf samtools-1.3.tar.bz2 && \
	cd /samtools-1.3 && \
	make && \
	chmod 777 /samtools-1.3/samtools && \
	mv /samtools-1.3/samtools /usr/local/bin/

RUN pip install git+https://github.com/outlierbio/ob-pipelines.git

ADD *.sh /
