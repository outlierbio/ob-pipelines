FROM centos:latest

RUN yum update -y && yum install -y \
	bzip2 \
	wget \
	md5sum

# Miniconda
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.1.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh
ENV PATH /opt/conda/bin:$PATH

# NCBI SRA toolkit
WORKDIR /opt
RUN wget --quiet https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/2.8.2-1/sratoolkit.2.8.2-1-centos_linux64.tar.gz && \
	tar -xvf sratoolkit.2.8.2-1-centos_linux64.tar.gz && \
	mv sratoolkit.2.8.2-1-centos_linux64 sratoolkit
ENV PATH /opt/sratoolkit/bin:$PATH

## Controlled access data only
# Add project credentials to sratoolkit, then point download dir to /scratch
# ADD secrets/* /opt/sratoolkit/
# RUN for f in $(ls /opt/sratoolkit/prj_*.ngc ); \
#	do \
#		vdb-config --import $f; \
#		prj=$(basename $f .ngc | sed 's/prj_//'); \
#		vdb-config --root --set repository/user/protected/dbGaP-$prj/root=/scratch; \
#	done

# parallel-fastq-dump to parallelize downloads
RUN conda install -c bioconda parallel-fastq-dump
RUN pip install awscli

VOLUME /scratch

ADD run.sh /
ENTRYPOINT ["sh", "/run.sh"]