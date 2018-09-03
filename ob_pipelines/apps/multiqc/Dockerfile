FROM outlierbio/ob-pipelines

MAINTAINER Jake Feala <jake@outlierbio.com>

RUN set -x && \
    conda install -y -c bioconda nomkl && \
    conda install -y -c bioconda multiqc

ADD multiqc.sh /

ENTRYPOINT ["sh", "/multiqc.sh"]
