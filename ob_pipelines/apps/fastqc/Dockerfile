FROM openjdk:8

RUN apt-get update && apt-get install -y python-pip
RUN pip install boto3

# Install FastQC
ADD http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.5.zip /
RUN unzip /fastqc_v0.11.5.zip && chmod 777 /FastQC/fastqc
ENV PATH /FastQC:$PATH

RUN pip install git+https://github.com/outlierbio/ob-pipelines

ENTRYPOINT ["s3wrap", "fastqc"]