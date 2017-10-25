FROM pipeline-base
MAINTAINER Jake Feala <jake@outlierbio.com>

RUN conda install -y -c bioconda nomkl
RUN conda install -y -c bioconda multiqc

ADD ./multiqc.sh /

ENTRYPOINT ["sh", "/multiqc.sh"]