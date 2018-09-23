import os.path as op

import luigi
from luigi.contrib.s3 import S3Target

from ob_pipelines.config import settings
from ob_pipelines.batch import BatchTask
from ob_pipelines.sample import Sample
from ob_pipelines.apps.sra.task import SRADownload


class FastQC(BatchTask, Sample):

    job_definition = 'fastqc'
    command = ['Ref::fq1', 'Ref::fq2', 'Ref::out_dir', 'Ref::name']
    image = 'outlierbio/fastqc'

    def requires(self):
        return SRADownload(
            srr_id=self.sample_id,
            layout=self.sample['layout'],
            outpath='s3://vl46-ngs-raw/sra')

    def output(self):
        s3_paths = {
            'html_1': self.sample_id + '_1_fastqc.html',
            'zip_1': self.sample_id + '_1_fastqc.zip',
            'html_2': self.sample_id + '_2_fastqc.html',
            'zip_2': self.sample_id + '_2_fastqc.zip'
        }
        return {k: S3Target('{}/{}/fastqc/{}'.format(settings.get_target_bucket(),
                            self.sample_folder, fname))
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
