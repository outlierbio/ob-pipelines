#!/usr/bin/env bash
REPO_DIR=`dirname $0`/..

FASTQC_VERSION=0.11.5
MEME_VERSION=4.12.0
MINICONDA_VERSION=4.5.4
KALISTO_VERSION=0.44.0
PICARD_VERSION=2.8.3
SAMTOOLS_VERSION=1.3
SKEWER_VERSION=0.2.2
STAR_VERSION=2.5.0b
SUBREAD_VERSION=1.6.2

docker build --no-cache -t outlierbio/ob-pipelines $REPO_DIR --build-arg MINICONDA_VERSION=${MINICONDA_VERSION}
docker build --no-cache -t outlierbio/bwa $REPO_DIR/ob_pipelines/apps/bwa
docker build --no-cache -t outlierbio/disambiguate $REPO_DIR/ob_pipelines/apps/disambiguate
docker build --no-cache -t outlierbio/fastqc $REPO_DIR/ob_pipelines/apps/fastqc --build-arg FASTQC_VERSION=${FASTQC_VERSION}
docker build --no-cache -t outlierbio/htseq $REPO_DIR/ob_pipelines/apps/htseq
docker build --no-cache -t outlierbio/kallisto $REPO_DIR/ob_pipelines/apps/kallisto --build-arg KALISTO_VERSION=${KALISTO_VERSION}
docker build --no-cache -t outlierbio/macs2 $REPO_DIR/ob_pipelines/apps/macs2
docker build --no-cache -t outlierbio/meme $REPO_DIR/ob_pipelines/apps/meme --build-arg MEME_VERSION=${MEME_VERSION}
docker build --no-cache -t outlierbio/multiqc $REPO_DIR/ob_pipelines/apps/multiqc
docker build --no-cache -t outlierbio/picard $REPO_DIR/ob_pipelines/apps/picard --build-arg PICARD_VERSION=${PICARD_VERSION}
docker build --no-cache -t outlierbio/pysam $REPO_DIR/ob_pipelines/apps/pysam
docker build --no-cache -t outlierbio/rseqc $REPO_DIR/ob_pipelines/apps/rseqc
docker build --no-cache -t outlierbio/samtools $REPO_DIR/ob_pipelines/apps/samtools --build-arg SAMTOOLS_VERSION=${SAMTOOLS_VERSION}
docker build --no-cache -t outlierbio/skewer $REPO_DIR/ob_pipelines/apps/skewer --build-arg SKEWER_VERSION=${SKEWER_VERSION}
docker build --no-cache -t outlierbio/star $REPO_DIR/ob_pipelines/apps/star --build-arg STAR_VERSION=${STAR_VERSION}
docker build --no-cache -t outlierbio/subread $REPO_DIR/ob_pipelines/apps/subread --build-arg SUBREAD_VERSION=${SUBREAD_VERSION}


docker push outlierbio/ob-pipelines
docker push outlierbio/bwa
docker push outlierbio/disambiguate
docker push outlierbio/fastqc
docker push outlierbio/htseq
docker push outlierbio/kallisto
docker push outlierbio/macs2
docker push outlierbio/meme
docker push outlierbio/multiqc
docker push outlierbio/picard
docker push outlierbio/pysam
docker push outlierbio/rseqc
docker push outlierbio/samtools
docker push outlierbio/skewer
docker push outlierbio/star
docker push outlierbio/subread
