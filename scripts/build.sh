#!/usr/bin/env bash
REPO_DIR=`dirname $0`/..

REGISTRY_URI=outlierbio  # Adjust for private Docker registry

FASTQC_VERSION=0.11.5
MEME_VERSION=4.12.0
MINICONDA_VERSION=4.5.4
KALISTO_VERSION=0.44.0
PICARD_VERSION=2.8.3
SAMTOOLS_VERSION=1.3
SKEWER_VERSION=0.2.2
SRA_VERSION=2.8.2-1
STAR_VERSION=2.5.0b
SUBREAD_VERSION=1.6.2
GDC_VERSION=1.3.0

docker build -t $REGISTRY_URI/ob-pipelines $REPO_DIR --build-arg MINICONDA_VERSION=${MINICONDA_VERSION}
docker build -t $REGISTRY_URI/bwa $REPO_DIR/ob_pipelines/apps/bwa
docker build -t $REGISTRY_URI/disambiguate $REPO_DIR/ob_pipelines/apps/disambiguate
docker build -t $REGISTRY_URI/fastqc $REPO_DIR/ob_pipelines/apps/fastqc --build-arg FASTQC_VERSION=${FASTQC_VERSION}
docker build -t $REGISTRY_URI/htseq $REPO_DIR/ob_pipelines/apps/htseq
docker build -t $REGISTRY_URI/kallisto $REPO_DIR/ob_pipelines/apps/kallisto --build-arg KALISTO_VERSION=${KALISTO_VERSION}
docker build -t $REGISTRY_URI/macs2 $REPO_DIR/ob_pipelines/apps/macs2
docker build -t $REGISTRY_URI/meme $REPO_DIR/ob_pipelines/apps/meme --build-arg MEME_VERSION=${MEME_VERSION}
docker build -t $REGISTRY_URI/multiqc $REPO_DIR/ob_pipelines/apps/multiqc
docker build -t $REGISTRY_URI/picard $REPO_DIR/ob_pipelines/apps/picard --build-arg PICARD_VERSION=${PICARD_VERSION}
docker build -t $REGISTRY_URI/pysam $REPO_DIR/ob_pipelines/apps/pysam
docker build -t $REGISTRY_URI/rseqc $REPO_DIR/ob_pipelines/apps/rseqc
docker build -t $REGISTRY_URI/samtools $REPO_DIR/ob_pipelines/apps/samtools --build-arg SAMTOOLS_VERSION=${SAMTOOLS_VERSION}
docker build -t $REGISTRY_URI/skewer $REPO_DIR/ob_pipelines/apps/skewer --build-arg SKEWER_VERSION=${SKEWER_VERSION}
docker build -t $REGISTRY_URI/sra $REPO_DIR/ob_pipelines/apps/sra --build-arg MINICONDA_VERSION=${MINICONDA_VERSION} --build-arg SRA_VERSION=${SRA_VERSION}
docker build -t $REGISTRY_URI/star $REPO_DIR/ob_pipelines/apps/star --build-arg STAR_VERSION=${STAR_VERSION}
docker build -t $REGISTRY_URI/subread $REPO_DIR/ob_pipelines/apps/subread --build-arg SUBREAD_VERSION=${SUBREAD_VERSION}
docker build -t $REGISTRY_URI/gdc $REPO_DIR/ob_pipelines/apps/gdc --build-arg GDC_VERSION=${GDC_VERSION}
docker build -t $REGISTRY_URI/s3sync $REPO_DIR/ob_pipelines/apps/s3sync


docker push $REGISTRY_URI/ob-pipelines
docker push $REGISTRY_URI/bwa
docker push $REGISTRY_URI/disambiguate
docker push $REGISTRY_URI/fastqc
docker push $REGISTRY_URI/htseq
docker push $REGISTRY_URI/kallisto
docker push $REGISTRY_URI/macs2
docker push $REGISTRY_URI/meme
docker push $REGISTRY_URI/multiqc
docker push $REGISTRY_URI/picard
docker push $REGISTRY_URI/pysam
docker push $REGISTRY_URI/rseqc
docker push $REGISTRY_URI/samtools
docker push $REGISTRY_URI/skewer
docker push $REGISTRY_URI/sra
docker push $REGISTRY_URI/star
docker push $REGISTRY_URI/subread
docker push $REGISTRY_URI/gdc
docker push $REGISTRY_URI/s3sync
