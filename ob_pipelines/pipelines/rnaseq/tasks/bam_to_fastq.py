from luigi.contrib.s3 import S3Target

from ob_pipelines.batch import BatchTask, LoggingTaskWrapper
from ob_pipelines.config import cfg
from ob_pipelines.entities.sample import Sample
from ob_pipelines.tasks.filter_spliced import FilterSpliced


class BamToFastQ(BatchTask, LoggingTaskWrapper, Sample):
    job_definition = 'bam2fastq'

    @property
    def parameters(self):
        return {
            'input': self.input().path,
            'fq1': self.output()['fq1'].path,
            'fq2': self.output()['fq2'].path,
        }

    def requires(self):
        return FilterSpliced(sample_id=self.sample_id)

    def output(self):
        s3_prefix = '{}/{}/filtered/{}'.format(
            cfg['S3_BUCKET'], self.sample_folder, self.sample_id)
        s3_paths = [
            s3_prefix + '_1.fq.gz',
            s3_prefix + '_2.fq.gz',
        ]
        return [S3Target(path) for path in s3_paths]
