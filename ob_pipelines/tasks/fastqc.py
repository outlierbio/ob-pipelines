from os import path as op

from luigi.contrib.s3 import S3Target

from ob_pipelines.batch import BatchTask, LoggingTaskWrapper
from ob_pipelines.config import cfg
from ob_pipelines.entities.sample import Sample
from ob_pipelines.tasks.sample_fastq import SampleFastQ


class FastQC(BatchTask, LoggingTaskWrapper, Sample):
    job_definition = 'fastqc'

    def requires(self):
        return SampleFastQ(sample_id=self.sample_id)

    def output(self):
        s3_paths = {
            'html_1': self.sample_id + '_1_fastqc.html',
            'zip_1': self.sample_id + '_1_fastqc.zip',
            'html_2': self.sample_id + '_2_fastqc.html',
            'zip_2': self.sample_id + '_2_fastqc.zip'
        }
        return {k: S3Target(
            '{bucket}/{sample}/fastqc/{folder_name}'.format(bucket=cfg['S3_BUCKET'], sample=self.sample_folder,
                                                            folder_name=fname))
                for k, fname in s3_paths.items()}

    @property
    def parameters(self):
        fq1, fq2 = [tgt.path for tgt in self.input()]
        out_dir = op.dirname(self.output()['html_1'].path) + '/'
        return {
            'fq1': fq1,
            'fq2': fq2,
            'out_dir': out_dir,
            'name': self.sample_id
        }
