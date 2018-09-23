import luigi
from luigi.contrib.batch import BatchTask

from ob_pipelines.config import settings
from ob_pipelines import LoggingTaskWrapper


class S3Sync(BatchTask, LoggingTaskWrapper):
    job_definition = 's3sync'
    sync_id = luigi.Parameter()

    done = False

    defS3path = settings.get_source_bucket() + '/reference'
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
