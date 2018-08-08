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
        md5sum /scratch/${srr}_1.fastq.gz > /scratch/${srr}_1.fastq.gz.md5
        md5sum /scratch/${srr}_2.fastq.gz > /scratch/${srr}_2.fastq.gz.md5
        aws s3 cp /scratch/${srr}_1.fastq.gz $s3_outpath
        aws s3 cp /scratch/${srr}_1.fastq.gz.md5 $s3_outpath
        aws s3 cp /scratch/${srr}_2.fastq.gz $s3_outpath
        aws s3 cp /scratch/${srr}_2.fastq.gz.md5 $s3_outpath
else
	parallel-fastq-dump \
                --sra-id=$srr \
                --threads 8 \
                --tmpdir /scratch \
                --outdir /scratch/ \
                --gzip;
        md5sum /scratch/${srr}.fastq.gz > /scratch/${srr}.fastq.gz.md5
        aws s3 cp /scratch/${srr}.fastq.gz $s3_outpath
        aws s3 cp /scratch/${srr}.fastq.gz.md5 $s3_outpath
fi

rm -rf /scratch/sra/$srr.*