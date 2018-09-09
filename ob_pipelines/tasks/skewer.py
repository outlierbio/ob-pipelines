from luigi.contrib.s3 import S3Target

from ob_pipelines.batch import BatchTask, LoggingTaskWrapper
from ob_pipelines.config import cfg, settings
from ob_pipelines.entities.sample import Sample
from ob_pipelines.tasks.sample_fastq import SampleFastQ


class Skewer(BatchTask, LoggingTaskWrapper, Sample):
    job_definition = 'skewer'

    def requires(self):
        return SampleFastQ(sample_id=self.sample_id)

    @property
    def parameters(self):
        fq1, fq2 = [tgt.path for tgt in self.input()]
        outdir = '{}/{}/skewer/'.format(settings.get_target_bucket(), self.sample_folder)
        return {
            'outdir': outdir,
            'fq1': fq1,
            'fq2': fq2
        }

    def output(self):
        outdir = '{}/{}/skewer/'.format(settings.get_target_bucket(), self.sample_folder)
        yield S3Target(outdir + 'trimmed-pair1.fastq.gz')
        yield S3Target(outdir + 'trimmed-pair2.fastq.gz')
