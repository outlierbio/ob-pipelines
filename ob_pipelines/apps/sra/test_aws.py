"""
Test deployment of the job on AWS Batch.

Requires an active cluster (if unmanaged compute environment). Start one with ob-cluster:

    $ ob-cluster start 1

Don't forget to shut it down:

    $ ob-cluster shutdown
"""
import os.path as op
from ob_pipelines.batch import BatchClient

bc = BatchClient()  # thin wrapper for boto3.client('batch')

# Register job definition if needed. Assumes local directory
bc.register_job_definition('./sra-job-definition.json')

parameters = {
    'srr_id': 'SRR2135322',
    'outpath': 's3://vl46-ngs-raw/test/'
}

job_id = bc.submit_job('sra', parameters)
bc.get_job_status(job_id)
bc.wait_on_job(job_id)