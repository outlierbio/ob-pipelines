FROM openjdk:8

RUN apt-get update && apt-get install -y python-pip
RUN pip install boto3 click

# Install FastQC
RUN wget http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.5.zip -O /fastqc_v0.11.5.zip && \
	unzip /fastqc_v0.11.5.zip && \
	chmod 777 /FastQC/fastqc
ENV PATH /FastQC:$PATH

VOLUME ["/scratch"]
ENV SCRATCH_DIR=/scratch

RUN pip install git+https://github.com/outlierbio/ob-pipelines

ADD ./fastqc.py /

ENTRYPOINT ["python", "/fastqc.py"]