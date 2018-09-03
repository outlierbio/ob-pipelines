from luigi.contrib.s3 import S3Target

from ob_pipelines.batch import BatchTask, LoggingTaskWrapper
from ob_pipelines.entities.sample import Sample
from ob_pipelines.pipelines.rnaseq.tasks.star import Star


class SortBam(BatchTask, LoggingTaskWrapper, Sample):
    job_definition = 'samtools-sort-by-coord'

    @property
    def parameters(self):
        return {
            'input': self.input()['bam'].path,
            'output': self.output().path,
            'tmp_prefix': '/scratch/{}'.format(self.sample_id)
        }

    def requires(self):
        return Star(sample_id=self.sample_id)

    def output(self):
        return S3Target(self.input()['bam'].path.replace('.bam', '.sorted.bam'))
