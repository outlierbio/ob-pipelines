from luigi import Parameter
from luigi.contrib.s3 import S3Target

from ob_pipelines.apps.star import STAR_OUTPUTS
from ob_pipelines.batch import BatchTask, LoggingTaskWrapper
from ob_pipelines.config import cfg
from ob_pipelines.entities.sample import Sample
from ob_pipelines.pipelines.rnaseq.rnaseq import get_index
from ob_pipelines.tasks.sample_fastq import SampleFastQ


class Star(BatchTask, LoggingTaskWrapper, Sample):
    job_definition = 'star'
    species = Parameter(default='human')

    @property
    def parameters(self):
        fq1, fq2 = [tgt.path for tgt in self.input()]
        return {
            'fq1': fq1,
            'fq2': fq2,
            'genome_dir': get_index('star', species=self.species),
            'prefix': self.prefix(),
            'threads': '20'
        }

    def prefix(self):
        return '{}/{}/star/{}'.format(
            cfg['S3_BUCKET'], self.sample_folder, self.sample_id + '.')

    def requires(self):
        return SampleFastQ(sample_id=self.sample_id)

    def output(self):
        s3_paths = {k: v.format(prefix=self.prefix()) for k, v in STAR_OUTPUTS.items()}
        return {k: S3Target(path) for k, path in s3_paths.items()}
