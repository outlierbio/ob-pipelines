import os.path as op

from luigi.contrib.s3 import S3Target
from luigi import Parameter, WrapperTask
import luigi

from ob_pipelines.apps.kallisto import merge_column
from ob_pipelines.batch import BatchTask
from ob_pipelines.config import cfg
from ob_pipelines.sample import get_samples, Sample
from ob_pipelines.s3 import csv_to_s3
from ob_pipelines.pipelines.rnaseq import Star, SampleFastQ, FastQC

class Skewer(BatchTask, Sample):

    job_definition = 'skewer'

    def requires(self):
        return SampleFastQ(sample_id=self.sample_id)

    @property
    def parameters(self):
        fq1, fq2 = [tgt.path for tgt in self.input()]
        outdir = '{}/{}/skewer/'.format(cfg['S3_BUCKET'], self.sample_folder)
        return {
            'outdir': outdir,
            'fq1': fq1,
            'fq2': fq2
        }

    def output(self):
        outdir = '{}/{}/skewer/'.format(cfg['S3_BUCKET'], self.sample_folder)
        yield S3Target(outdir + 'trimmed-pair1.fastq.gz')
        yield S3Target(outdir + 'trimmed-pair2.fastq.gz')


class FastQCTrimmed(FastQC):

    def requires(self):
        return Skewer(sample_id=self.sample_id)


class StarBySpecies(Star):

    def requires(self):
        return Skewer(sample_id=self.sample_id)

    def prefix(self):        
        return '{}/{}/star/{}.{}.'.format(
            cfg['S3_BUCKET'],self.sample_folder, self.sample_id, self.species)


class DisambiguateHumanMouse(BatchTask, Sample):
    
    job_definition = 'disambiguate'
    
    @property
    def parameters(self):
        outdir = '{}/{}/disambiguate/'.format(cfg['S3_BUCKET'], self.sample_folder)
        return {
            'outdir': outdir,
            'sample': self.sample_id,
            'aligner': 'star',
            'A': self.input()['human']['bam'].path,
            'B': self.input()['mouse']['bam'].path
        }

    def requires(self):
        return {
            'human': StarBySpecies(sample_id=self.sample_id, species='human'),
            'mouse': StarBySpecies(sample_id=self.sample_id, species='mouse')
        }

    def output(self):
        output_files = {
            'human': '{}{}.disambiguatedSpeciesA.bam',
            'mouse': '{}{}.disambiguatedSpeciesB.bam',
            'human_ambiguous': '{}{}.ambiguousSpeciesA.bam',
            'mouse_ambiguous': '{}{}.ambiguousSpeciesB.bam',
            'summary': '{}{}_summary.txt'
        }
        s3_paths = {k: v.format(self.parameters['outdir'], self.parameters['sample'])
                    for k, v in output_files.items()}
        return {k: S3Target(path) for k, path in s3_paths.items()}


class BamToFastq(BatchTask, Sample):

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


class Run(WrapperTask):

    expt_id = Parameter()

    def requires(self):
        #for sample_id in get_samples(self.expt_id):
            #yield FastQCTrimmed(sample_id=sample_id)
            #yield BamToFastq(sample_id=sample_id)
        
        yield MergeERCC(expt_id=self.expt_id)


if __name__ == '__main__':
    luigi.run(local_scheduler=True)