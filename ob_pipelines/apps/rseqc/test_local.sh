# Set some parameters for local use. 
# Make sure your AWS keys are set as env vars for this test.
SCRATCH_DIR=~/Desktop/scratch
NGS_BUCKET=
REF_BUCKET=

docker build -t rseqc .

mkdir -p $SCRATCH_DIR

# Run RSeQC from S3 files (requires BAM index in same folder)
docker run \
	-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
	-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
	-v $SCRATCH_DIR:/scratch \
	rseqc \
		gene_coverage \
		$NGS_BUCKET/test/chr21.1e4.Aligned.sortedByCoord.out.bam \
		$REF_BUCKET/rseqc/hg38_GENCODE_v24_basic.bed \
		$NGS_BUCKET/test/rseqc/chr21.1e4

# Run RSeQC read_distribution
docker run \
	-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
	-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
	-v $SCRATCH_DIR:/scratch \
	rseqc \
		read_distribution \
		$NGS_BUCKET/test/chr21.1e4.Aligned.sortedByCoord.out.bam \
		$REF_BUCKET/rseqc/hg38_GENCODE_v24_basic.bed \
		$NGS_BUCKET/test/chr21.1e4/rseqc/chr21.1e4
