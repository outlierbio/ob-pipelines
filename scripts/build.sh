REPO_DIR=`dirname $0`/..

docker build --no-cache -t outlierbio/ob-pipelines $REPO_DIR
docker build --no-cache -t outlierbio/star $REPO_DIR/ob_pipelines/apps/star
docker build --no-cache -t outlierbio/samtools $REPO_DIR/ob_pipelines/apps/samtools
docker build --no-cache -t outlierbio/kallisto $REPO_DIR/ob_pipelines/apps/kallisto
docker build --no-cache -t outlierbio/fastqc $REPO_DIR/ob_pipelines/apps/fastqc
docker build --no-cache -t outlierbio/rseqc $REPO_DIR/ob_pipelines/apps/rseqc
docker build --no-cache -t outlierbio/picard $REPO_DIR/ob_pipelines/apps/picard


docker push outlierbio/ob-pipelines
docker push outlierbio/star
docker push outlierbio/samtools
docker push outlierbio/kallisto
docker push outlierbio/fastqc
docker push outlierbio/rseqc
docker push outlierbio/picard