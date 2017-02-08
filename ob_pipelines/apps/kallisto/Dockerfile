FROM outlierbio/ob-pipelines
MAINTAINER Jake Feala <jake@outlierbio.com>

RUN wget https://github.com/pachterlab/kallisto/releases/download/v0.43.0/kallisto_linux-v0.43.0.tar.gz && \
  tar -xvf kallisto_linux-v0.43.0.tar.gz && \
  cp kallisto_linux-v0.43.0/kallisto /usr/local/bin

ENTRYPOINT ["s3wrap", "kallisto"]