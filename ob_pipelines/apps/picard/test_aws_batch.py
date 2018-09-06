import os.path as op

import ob_pipelines
from ob_pipelines.batch import BatchClient

module_dir = op.dirname(ob_pipelines.__file__)  # __file__ is __init__.py, have to get parent folder

bc = BatchClient()  # thin wrapper for boto3.client('batch')

# assuming job definition is already registered

parameters = {
    'input': 's3://c4t-data/GE-2/GS-31/disambiguate/GS-31.disambiguatedSpeciesA.bam',
    'fq1': 's3://c4t-data/GE-2/GS-31/disambiguate/GS-31_1.fq.gz',
    'fq2': 's3://c4t-data/GE-2/GS-31/disambiguate/GS-31_2.fq.gz'
}

job_id = bc.submit_job('bam2fastq', parameters)
bc.get_job_status(job_id)
bc.wait_on_job(job_id)