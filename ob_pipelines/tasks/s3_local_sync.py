import luigi
from luigi import LocalTarget

from ob_pipelines.config import cfg
from ob_pipelines import LoggingTaskWrapper


class S3Syc(LoggingTaskWrapper):

    job_definition = 's3sync'
    sync_id = luigi.Parameter()
    s3_bucket = luigi.Parameter(default=cfg['S3_BUCKET'])

    @property
    def job_name(self):
        return '{}-s3sync'.format(self.sync_id)

    @property
    def parameters(self):
        return {
            'sync_id': self.sync_id,
            's3_bucket': self.s3_bucket
        }

    def output(self):
        return LocalTarget('/reference')