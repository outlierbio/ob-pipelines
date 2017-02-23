DIR=`dirname $0`

docker build --no-cache -t outlierbio/ob-pipelines $DIR
docker build --no-cache -t outlierbio/star $DIR/ob_pipelines/apps/star
docker build --no-cache -t outlierbio/samtools $DIR/ob_pipelines/apps/samtools
docker build --no-cache -t outlierbio/kallisto $DIR/ob_pipelines/apps/kallisto
docker build --no-cache -t outlierbio/fastqc $DIR/ob_pipelines/apps/fastqc
docker build --no-cache -t outlierbio/rseqc $DIR/ob_pipelines/apps/rseqc
docker build --no-cache -t outlierbio/picard $DIR/ob_pipelines/apps/picard


docker push outlierbio/ob-pipelines
docker push outlierbio/star
docker push outlierbio/samtools
docker push outlierbio/kallisto
docker push outlierbio/fastqc
docker push outlierbio/rseqc
docker push outlierbio/picard