FROM outlierbio/ob-pipelines

MAINTAINER Jake Feala <jake@outlierbio.com>

RUN conda install -c bioconda ngs-disambiguate

ENTRYPOINT ["s3wrap", "-r", "ngs_disambiguate"]
