FROM outlierbio/ob-pipelines

ADD ./subread-1.5.3-Linux-x86_64.tar.gz /
ENV PATH /subread-1.5.3-Linux-x86_64/bin:$PATH

RUN pip install git+https://github.com/outlierbio/ob-pipelines

ENTRYPOINT ["s3wrap", "featureCounts"]
