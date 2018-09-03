from luigi.contrib.s3 import S3Target

from ob_pipelines.batch import BatchTask, LoggingTaskWrapper
from ob_pipelines.config import cfg
from ob_pipelines.entities.sample import Sample
from ob_pipelines.pipelines.xenograft.tasks.disambiguate_human_mouse import DisambiguateHumanMouse


class BamToFastQ(BatchTask, LoggingTaskWrapper, Sample):
    job_definition = 'bam2fastq'

    @property
    def parameters(self):
        return {
            'input': self.input()['human'].path,
            'fq1': self.output()['fq1'].path,
            'fq2': self.output()['fq2'].path,
        }

    def requires(self):
        return DisambiguateHumanMouse(sample_id=self.sample_id)

    def output(self):
        s3_prefix = '{}/{}/disambiguate/{}'.format(
            cfg['S3_BUCKET'], self.sample_folder, self.sample_id)
        s3_paths = {
            'fq1': s3_prefix + '_1.fq.gz',
            'fq2': s3_prefix + '_2.fq.gz',
        }
        return {k: S3Target(path) for k, path in s3_paths.items()}
