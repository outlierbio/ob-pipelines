srr=$1
layout=$2
s3_outpath=$3

cd /scratch

if [ $layout = "paired" ]; then
        parallel-fastq-dump \
                --sra-id=$srr \
                --threads 8 \
                --tmpdir /scratch \
                --outdir /scratch/ \
                --gzip \
                --split-files;
        aws s3 cp /scratch/${srr}_1.fastq.gz $s3_outpath
        aws s3 cp /scratch/${srr}_2.fastq.gz $s3_outpath
else
	parallel-fastq-dump \
                --sra-id=$srr \
                --threads 8 \
                --tmpdir /scratch \
                --outdir /scratch/ \
                --gzip;
        aws s3 cp /scratch/${srr}.fastq.gz $s3_outpath
fi

rm -rf /scratch/sra/$srr.*