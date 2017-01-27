FROM outlierbio/ob-pipelines
MAINTAINER Jake Feala <jake@outlierbio.com>

RUN wget https://github.com/alexdobin/STAR/releases/download/2.5.0b/Linux_x86_64_static_gcc.tgz && \
  tar -xvzf Linux_x86_64_static_gcc.tgz && \
  cp Linux_x86_64_static_gcc5.3.0/STAR /bin

ADD star.py /

ENTRYPOINT ["python", "/star.py"]
