import luigi
from luigi import LocalTarget
from luigi.contrib.batch import BatchTask

from ob_pipelines.config import cfg
from ob_pipelines import LoggingTaskWrapper


class S3Sync(BatchTask, LoggingTaskWrapper):

    job_definition = 's3sync'
    sync_id = luigi.Parameter()
    defS3path = cfg['RAW_BUCKET'] + '/reference'
    s3_bucket = luigi.Parameter(default=defS3path)

    @property
    def job_name(self):
        return '{}-s3sync'.format(self.sync_id)

    @property
    def parameters(self):
        return {
            'sync_id': self.sync_id,
            's3_bucket': self.s3_bucket
        }

    def complete(self):
        return False

    def output(self):
        return LocalTarget('/reference')