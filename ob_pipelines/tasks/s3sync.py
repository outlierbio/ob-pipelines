import luigi
from luigi import LocalTarget
from luigi.contrib.batch import BatchTask

from ob_pipelines.config import cfg
from ob_pipelines import LoggingTaskWrapper


class S3Sync(BatchTask, LoggingTaskWrapper):
    job_definition = 's3sync'
    sync_id = luigi.Parameter()

    done = False

    defS3path = cfg['RAW_BUCKET'] + '/reference'
    source = luigi.Parameter(default=defS3path)
    destination = luigi.Parameter(default='')

    @property
    def job_name(self):
        return '{}-s3sync'.format(self.sync_id)

    @property
    def parameters(self):
        return {
            'sync_id': self.sync_id,
            'source': self.source,
            'destination': self.destination
        }

    def complete(self):
        return self.done

    def run(self):
        self.done = True
