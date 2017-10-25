import logging
import os.path as op

from luigi.contrib.s3 import S3Target
from luigi import Parameter, BoolParameter, ExternalTask, Task, WrapperTask

from ob_pipelines.config import cfg
from ob_pipelines.sample import Sample, get_samples
from ob_pipelines.s3 import csv_to_s3
from ob_pipelines.batch import BatchTask
from ob_pipelines.apps.star import STAR_OUTPUTS
from ob_pipelines.apps.rseqc import GENE_COVERAGE_OUTPUTS
from ob_pipelines.apps.kallisto import merge_column

logger = logging.getLogger('luigi-interface')


def get_index(tool, species='human', build='latest'):
    indexes = {
        'star': {
            'human': {
                'test': '/reference/star/b38.chr21.gencode_v25.101',
                'latest': '/reference/star/b38.gencode_v25.101'
            },
            'mouse': {
                'latest': '/reference/star/m38.gencode_vM12.101'
            }
        },
        'kallisto': {
            'human': {
                'test': '/reference/kallisto/gencode_v25.chr21/gencode_v25.chr21.idx',
                'latest': '/reference/kallisto/gencode_v25/gencode.v25.ercc.idx'
            }
        }
    }
    return indexes[tool][species][build]


class SampleFastQ(ExternalTask, Sample):
    def output(self):
        yield S3Target(self.sample['FastQ 1'])
        yield S3Target(self.sample['FastQ 2'])


class FastQC(BatchTask, Sample):

    job_definition = 'fastqc'
    command = ['Ref::fq1', 'Ref::fq2', 'Ref::out_dir', 'Ref::name']
    image = 'outlierbio/fastqc'

    def requires(self):
        return SampleFastQ(sample_id=self.sample_id)

    def output(self):
        s3_paths = {
            'html_1': self.sample_id + '_1_fastqc.html',
            'zip_1': self.sample_id + '_1_fastqc.zip',
            'html_2': self.sample_id + '_2_fastqc.html',
            'zip_2': self.sample_id + '_2_fastqc.zip'
        }
        return {k: S3Target('{}/{}/fastqc/{}'.format(cfg['S3_BUCKET'], self.sample_folder, fname))
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


class Star(BatchTask, Sample):

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


class SortBam(BatchTask, Sample):

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


class IndexBam(BatchTask, Sample):

    job_definition = 'samtools-index'
    image = 'outlierbio/samtools'
    command = ['index', 'Ref::input', 'Ref::output']

    @property
    def parameters(self):
        return {
            'input': self.input().path, 
            'output': self.output().path
        }

    def requires(self):
        return SortBam(sample_id=self.sample_id)

    def output(self):
        return S3Target(self.input().path + '.bai')


class GeneCoverage(BatchTask, Sample):

    job_definition = 'gene-coverage'

    def prefix(self):
        return '{}/{}/rseqc/{}'.format(
            cfg['S3_BUCKET'], self.sample_folder, self.sample_id)

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


class ReadDistribution(BatchTask, Sample):

    job_definition = 'read-distribution'

    @property
    def parameters(self):
        return {
            'bedfile': '/reference/rseqc/hg38_RefSeq.bed',
            'input': self.input()[0].path,
            'output': self.output().path
        }

    def requires(self):
        return SortBam(sample_id=self.sample_id), IndexBam(sample_id=self.sample_id)

    def output(self):
        return S3Target('{}/{}/rseqc/{}.read_distribution.txt'.format(
            cfg['S3_BUCKET'], self.sample_folder, self.sample_id))


class FilterSpliced(BatchTask, Sample):

    job_definition = 'filter-spliced'

    @property
    def parameters(self):
        return {
            'input': self.input()[0].path,
            'output': self.output().path
        }

    def requires(self):
        return SortBam(sample_id=self.sample_id), IndexBam(sample_id=self.sample_id)

    def output(self):
        return S3Target('{}/{}/filtered/{}.spliced_reads.bam'.format(
            cfg['S3_BUCKET'], self.sample_folder, self.sample_id))


class BamToFastq(BatchTask, Sample):

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


class ERCCQuant(BatchTask, Sample):
    
    job_definition = 'kallisto'

    @property
    def parameters(self):
        fq1, fq2 = self.input()
        return {
            'threads': '20',
            'index': '/reference/kallisto/ercc.idx',
            'reads1': fq1.path,
            'reads2': fq2.path,
            'strand_flag': '--rf-stranded',
            'output': op.dirname(self.output()['abundance'].path) + '/'
        }

    def requires(self):
        return SampleFastQ(sample_id=self.sample_id)

    def output(self):
        output_files = {
                'abundance': 'abundance.tsv',
                'h5': 'abundance.h5',
                'run_info': 'run_info.json'
        }
        return {k: S3Target('{}/{}/ercc-rev-strand/{}'.format(cfg['S3_BUCKET'], self.sample_folder, fname))
                for k, fname in output_files.items()}


class Kallisto(BatchTask, Sample):
    
    job_definition = 'kallisto'

    @property
    def parameters(self):
        fq1, fq2 = self.input()
        return {
            'threads': '20',
            'index': get_index('kallisto'),
            'reads1': fq1.path,
            'reads2': fq2.path,
            'strand_flag': '--rf-stranded',
            'output': op.dirname(self.output()['abundance'].path) + '/'
        }

    def requires(self):
        return SampleFastQ(sample_id=self.sample_id)

    def output(self):
        output_files = {
                'abundance': 'abundance.tsv',
                'h5': 'abundance.h5',
                'run_info': 'run_info.json'
        }
        return {k: S3Target('{}/{}/kallisto/{}'.format(cfg['S3_BUCKET'], self.sample_folder, fname))
                for k, fname in output_files.items()}


class KallistoSpliced(Kallisto):

    def requires(self):
        return BamToFastq(sample_id=self.sample_id)

    def output(self):
        output_files = {
                'abundance': 'abundance.tsv',
                'h5': 'abundance.h5',
                'run_info': 'run_info.json'
        }
        return {k: S3Target('{}/{}/filtered/{}'.format(cfg['S3_BUCKET'], self.sample_folder, fname))
                for k, fname in output_files.items()}


class MergeKallisto(Task):

    expt_id = Parameter()
    annot = BoolParameter(False)

    def requires(self):
        return {
            sample_id: Kallisto(sample_id=sample_id)
            for sample_id in get_samples(self.expt_id)
        }

    def output(self):
        prefix = '{}/{}/'.format(cfg['S3_BUCKET'], self.expt_id)
        out_dict = {
            'est_counts': S3Target(prefix + 'est_counts.csv'),
            'tpm': S3Target(prefix + 'tpm.csv')
        }
        if self.annot:
            out_dict['annotations'] = S3Target(prefix + 'annotations.csv')
        return out_dict

    def run(self):
        # Gather input filepaths and labels
        tgt_dict = self.input()
        sample_ids = list(tgt_dict.keys())
        fpaths = [tgt_dict[sample_id]['abundance'].path for sample_id in sample_ids]

        # Merge columns
        annotations, est_counts = merge_column(fpaths, sample_ids, data_col='est_counts', annot=self.annot)
        annotations, tpm = merge_column(fpaths, sample_ids, data_col='tpm', annot=self.annot)

        if self.annot:
            csv_to_s3(annotations, self.output()['annotations'].path)
        csv_to_s3(est_counts, self.output()['est_counts'].path)
        csv_to_s3(tpm, self.output()['tpm'].path)


class MergeERCC(Task):

    expt_id = Parameter()

    def requires(self):
        return {
            sample_id: ERCCQuant(sample_id=sample_id)
            for sample_id in get_samples(self.expt_id)
        }

    def output(self):
        prefix = '{}/{}/'.format(cfg['S3_BUCKET'], self.expt_id)
        return {
            'est_counts': S3Target(prefix + 'ercc.unstranded.est_counts.csv'),
            'tpm': S3Target(prefix + 'ercc.unstranded.tpm.csv')
        }

    def run(self):
        # Gather input filepaths and labels
        tgt_dict = self.input()
        sample_ids = list(tgt_dict.keys())
        fpaths = [tgt_dict[sample_id]['abundance'].path for sample_id in sample_ids]

        # Merge columns
        annotations, est_counts = merge_column(fpaths, sample_ids, data_col='est_counts', annot=False)
        annotations, tpm = merge_column(fpaths, sample_ids, data_col='tpm', annot=False)

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
            yield ReadDistribution(sample_id=sample_id)
            yield KallistoSpliced(sample_id=sample_id)
        yield MergeKallisto(expt_id=self.expt_id)
        yield MergeERCC(expt_id=self.expt_id)

