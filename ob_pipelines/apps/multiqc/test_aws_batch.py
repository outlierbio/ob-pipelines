import os.path as op
import ob_pipelines
from ob_pipelines.batch import BatchClient

module_dir = op.dirname(ob_pipelines.__file__)  # __file__ is __init__.py, have to get parent folder

bc = BatchClient()  # thin wrapper for boto3.client('batch')

# Register job definition if needed
job_def = op.join(module_dir, 'apps', 'multiqc', 'job-definition.json')
bc.register_job_definition(job_def)

parameters = {
    'analysis_dir': 's3://com-dnli-ngs/test/1e4/'
}

job_id = bc.submit_job('multiqc', parameters)
bc.get_job_status(job_id)
bc.wait_on_job(job_id)