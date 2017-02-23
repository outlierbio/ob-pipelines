import logging
import os
import os.path as op

from luigi.s3 import S3Target, S3PathTask
from luigi import Parameter, BoolParameter, Task, WrapperTask
from ob_airtable import get_record_by_name, get_record
import requests

from ob_pipelines.s3 import csv_to_s3
from ob_pipelines.batch import BatchTask
from ob_pipelines.apps.star import STAR_OUTPUTS
from ob_pipelines.apps.kallisto import merge_column

logger = logging.getLogger('luigi-interface')

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
API_ENDPOINT = os.environ.get('AIRTABLE_API_ENDPOINT')
AIRTABLE_EXPT_TABLE = 'Genomics%20Expt'
AIRTABLE_SAMPLE_TABLE = 'Genomics%20Sample'

S3_BUCKET = os.environ.get('S3_BUCKET')
DOCKER_RUN = [
    'docker', 'run',
    '-e', 'AWS_ACCESS_KEY_ID=' + os.environ['AWS_ACCESS_KEY_ID'],
    '-e', 'AWS_SECRET_ACCESS_KEY=' + os.environ['AWS_SECRET_ACCESS_KEY'],
    '-e', 'SCRATCH_DIR=/scratch',
    '-v', '/tmp:/scratch']
THREADS = 2



def get_index(tool, species='human', build='latest'):
    indexes = {
        'star': {
            'human': {
                'test': '/reference/star/b38.chr21',
                'latest': '/reference/star/b38.gencode_v25.101'
            }
        },
        'kallisto': {
            'human': {
                'test': '/reference/kallisto/gencode_v25.chr21/gencode_v25.chr21.idx',
                'latest': '/reference/kallisto/gencode_v25/gencode_v25.idx'
            }
        }
    }
    return indexes[tool][species][build]


def get_samples(expt_id):
    expt = get_record_by_name(expt_id, AIRTABLE_EXPT_TABLE)
    sample_keys = expt['fields']['Genomics samples']

    for sample_key in sample_keys:
        sample = get_record(sample_key, AIRTABLE_SAMPLE_TABLE)
        yield sample['fields']['Name']


class Sample(object):

    sample_id = Parameter()

    @property
    def sample(self):
        if not hasattr(self, '_sample'):
            self._sample = get_record_by_name(self.sample_id, AIRTABLE_SAMPLE_TABLE)['fields']
        return self._sample

    @property
    def sample_folder(self):
        return '{expt}/{sample}'.format(
            bucket=S3_BUCKET,
            expt = self.experiment['Name'],
            sample=self.sample_id)

    @property
    def experiment(self):
        if not hasattr(self, '_experiment'):
            expt_key = self.sample['Experiment'][0]
            self._experiment = get_record(expt_key, AIRTABLE_EXPT_TABLE)['fields']
        return self._experiment


class PipelineTask(BatchTask):

    local = BoolParameter(False, significant=False)

    @property
    def job_name(self):
        return '{}-{}'.format(self.task_family, self.sample_id)


class FastQC(PipelineTask, Sample):

    job_definition = 'fastqc'
    command = ['Ref::fq1', 'Ref::fq2', 'Ref::out_dir', 'Ref::name']
    image = 'outlierbio/fastqc'

    def requires(self):
        return (S3PathTask(path=self.sample['FastQ 1']),
                S3PathTask(path=self.sample['FastQ 2']))

    def output(self):
        s3_paths = {
            'html_1': self.sample_id + '_1_fastqc.html',
            'zip_1': self.sample_id + '_1_fastqc.zip',
            'html_2': self.sample_id + '_2_fastqc.html',
            'zip_2': self.sample_id + '_2_fastqc.zip'
        }
        return {k: S3Target('s3://{}/{}/fastqc/{}'.format(S3_BUCKET, self.sample_folder, fname))
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


class UpdateFastQC(Task, Sample):
    pass


class Star(PipelineTask, Sample):

    job_definition = 'star'
    image = 'outlierbio/star'
    command = ["star_align", "Ref::fq1", "Ref::fq2", "Ref::genome_dir", 
               "Ref::prefix", "Ref::threads"]

    @property
    def parameters(self):
        fq1, fq2 = [tgt.path for tgt in self.input()]
        return {
            'fq1': fq1,
            'fq2': fq2,
            'genome_dir': get_index('star'),
            'prefix': self.prefix(),
            'threads': '5' if self.local else '20'
        }

    def prefix(self):        
        return 's3://{}/{}/star/{}'.format(
            S3_BUCKET, self.sample_folder, self.sample_id + '.')

    def requires(self):
        return (S3PathTask(path=self.sample['FastQ 1']),
                S3PathTask(path=self.sample['FastQ 2']))

    def output(self):
        s3_paths = {k: v.format(prefix=self.prefix()) for k, v in STAR_OUTPUTS.items()}
        return {k: S3Target(path) for k, path in s3_paths.items()}


class IndexBam(PipelineTask, Sample):

    job_definition = 'samtools-index'
    image = 'outlierbio/samtools'
    command = ['index', 'Ref::input', 'Ref::output']

    @property
    def parameters(self):
        return {
            'input': self.input()['bam'].path, 
            'output': self.output().path
        }

    def requires(self):
        return Star(sample_id=self.sample_id)

    def output(self):
        return S3Target(self.input()['bam'].path + '.bai')


class GeneCoverage(PipelineTask, Sample):

    job_definition = 'gene-coverage'
    image = 'outlierbio/rseqc'
    command = [
        'geneBody_coverage.py',
        '-r', 'Ref::bedfile',
        '-i', 'Ref::input', 
        '-o', 'Ref::output'
    ]

    @property
    def parameters(self):
        return {
            'bedfile': '/hg38.housekeeping.bed',
            'input': self.input()['bam'].path, 
            'output': self.output().path
        }

    def requires(self):
        return Star(sample_id=self.sample_id)

    def output(self):
        return S3Target('s3://{}/{}/rseqc/geneBody_coverage.png'.format(
            S3_BUCKET, self.sample_folder))


class Kallisto(PipelineTask, Sample):
    
    job_definition = 'kallisto'
    image = 'outlierbio/kallisto'
    command = [
            "quant",
            "-i", "Ref::index",
            "-o", "Ref::output",
            "-t", "Ref::threads",
            "Ref::reads1", 
            "Ref::reads2"
    ]

    @property
    def parameters(self):
        fq1, fq2 = self.input()
        return {
            'threads': '20',
            'index': get_index('kallisto'),
            'reads1': fq1.path,
            'reads2': fq2.path,
            'output': op.dirname(self.output()['abundance'].path) + '/'
        }

    def requires(self):
        return (S3PathTask(path=self.sample['FastQ 1']),
                S3PathTask(path=self.sample['FastQ 2']))

    def output(self):
        output_files = {
                'abundance': 'abundance.tsv',
                'h5': 'abundance.h5',
                'run_info': 'run_info.json'
        }
        return {k: S3Target('s3://{}/{}/kallisto/{}'.format(S3_BUCKET, self.sample_folder, fname))
                for k, fname in output_files.items()}


class MergeKallisto(Task):

    expt_id = Parameter()

    def requires(self):
        return {
            sample_id: Kallisto(sample_id=sample_id)
            for sample_id in get_samples(self.expt_id)
        }

    def output(self):
        prefix = 's3://{}/{}/'.format(S3_BUCKET, self.expt_id)
        return {
            'annotations': S3Target(prefix + 'annotations.csv'),
            'est_counts': S3Target(prefix + 'est_counts.csv'),
            'tpm': S3Target(prefix + 'tpm.csv')
        }

    def run(self):
        # Gather input filepaths and labels
        tgt_dict = self.input()
        sample_ids = list(tgt_dict.keys())
        fpaths = [tgt_dict[sample_id]['abundance'].path for sample_id in sample_ids]

        # Merge columns
        annotations, est_counts = merge_column(fpaths, sample_ids, data_col='est_counts')
        annotations, tpm = merge_column(fpaths, sample_ids, data_col='tpm')

        csv_to_s3(annotations, self.output()['annotations'].path)
        csv_to_s3(est_counts, self.output()['est_counts'].path)
        csv_to_s3(tpm, self.output()['tpm'].path)


class RnaSeq(WrapperTask):

    expt_id = Parameter()

    def requires(self):
        for sample_id in get_samples(self.expt_id):
            yield FastQC(sample_id=sample_id)
            yield Star(sample_id=sample_id)
            yield IndexBam(sample_id=sample_id)
            yield Kallisto(sample_id=sample_id)
            yield GeneCoverage(sample_id=sample_id)


