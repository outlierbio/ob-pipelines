FROM outlierbio/ob-pipelines

RUN conda install -c bioconda ngs-disambiguate

RUN pip install git+https://github.com/outlierbio/ob-pipelines

ENTRYPOINT ["s3wrap", "-r", "ngs_disambiguate"]
