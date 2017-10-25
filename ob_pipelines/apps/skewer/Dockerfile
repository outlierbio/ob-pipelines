FROM outlierbio/ob-pipelines

RUN wget -O skewer https://sourceforge.net/projects/skewer/files/Binaries/skewer-0.2.2-linux-x86_64/download && \
 	chmod 555 skewer && \
 	mv skewer /usr/local/bin

RUN pip install git+https://github.com/outlierbio/ob-pipelines.git

ENTRYPOINT ["s3wrap", "skewer"]