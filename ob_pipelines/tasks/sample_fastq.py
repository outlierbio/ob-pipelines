from luigi import ExternalTask
from luigi.contrib.s3 import S3Target

from ob_pipelines import LoggingTaskWrapper
from ob_pipelines.entities.sample import Sample


class SampleFastQ(ExternalTask, LoggingTaskWrapper, Sample):
    def output(self):
        yield S3Target(self.sample['FastQ 1'])
        yield S3Target(self.sample['FastQ 2'])
