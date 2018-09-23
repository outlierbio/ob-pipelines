from luigi.contrib.s3 import S3Target

from ob_pipelines.apps.rseqc import GENE_COVERAGE_OUTPUTS
from ob_pipelines.batch import BatchTask, LoggingTaskWrapper
from ob_pipelines.config import settings
from ob_pipelines.entities.sample import Sample
from ob_pipelines.tasks.index_bam import IndexBam
from ob_pipelines.tasks.sort_bam import SortBam


class GeneCoverage(BatchTask, LoggingTaskWrapper, Sample):
    job_definition = 'gene-coverage'

    def prefix(self):
        return '{}/{}/rseqc/{}'.format(
            settings.get_target_bucket(), self.sample_folder, self.sample_id)

    @property
    def parameters(self):
        bam, bai = self.input()
        return {
            'bedfile': '/reference/rseqc/hg38.HouseKeepingGenes.bed',
            'input': bam.path,
            'output': self.prefix()
        }

    def requires(self):
        return SortBam(sample_id=self.sample_id), IndexBam(sample_id=self.sample_id)

    def output(self):
        s3_paths = {k: v.format(prefix=self.prefix()) for k, v in GENE_COVERAGE_OUTPUTS.items()}
        return {k: S3Target(path) for k, path in s3_paths.items()}
