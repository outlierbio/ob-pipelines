import boto3
import luigi

from ob_pipelines.pipelines.rnaseq.tasks.kallisto import Kallisto
from ob_pipelines.s3 import path_to_bucket_and_key

TEST_SAMPLE = 'GS-1'

s3 = boto3.client('s3')

t = Kallisto(sample_id=TEST_SAMPLE)
for s3_tgt in t.output().values():
	bucket, key = path_to_bucket_and_key(s3_tgt.path)
	s3.delete_object(Bucket=bucket, Key=key)

luigi.build([t], local_scheduler=True)

