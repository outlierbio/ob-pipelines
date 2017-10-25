FROM pipeline-base
MAINTAINER Jake Feala <jake@outlierbio.com>

RUN conda install -y -c bioconda nomkl
RUN conda install -y -c bioconda htseq

ADD ./htseq.sh /

ENTRYPOINT ["sh", "/htseq.sh"]