import logging
import os
import os.path as op
import re
from subprocess import check_output
from tempfile import mkdtemp, mkstemp

from luigi.s3 import S3Target, S3PathTask
from luigi import Parameter, Task, WrapperTask, ExternalTask
import requests

from ob_pipelines.s3 import s3, path_to_bucket_and_key
from ob_pipelines.apps.star import STAR_OUTPUTS

logger = logging.getLogger('luigi-interface')

AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY')
API_ENDPOINT = os.environ.get('AIRTABLE_API_ENDPOINT')
S3_BUCKET = os.environ.get('S3_BUCKET')
DOCKER_RUN = [
    'docker', 'run',
    '-e', 'AWS_ACCESS_KEY_ID=' + os.environ['AWS_ACCESS_KEY_ID'],
    '-e', 'AWS_SECRET_ACCESS_KEY=' + os.environ['AWS_SECRET_ACCESS_KEY'],
    '-e', 'SCRATCH_DIR=/scratch',
    '-v', '/tmp:/scratch']
THREADS = 2


def run_logged(cmd):
    """Wrap subprocess.check_output with logs"""    
    logger.info('Running: {}'.format(' '.join(cmd)))
    out = check_output(cmd)
    logger.info(out.decode())


def get_index(tool, species='human', build='latest'):
    indexes = {
        'star': {
            'human': {
                'test': '/scratch/star.b38.chr21',
                'latest': '/reference/star/b38.gencode_v25.101'
            }
        },
        'kallisto': {
            'human': {
                'test': '/scratch/gencode_v25.chr21.idx',
                'latest': '/reference/kallisto/gencode_v25/gencode_v25.idx'
            }
        }
    }
    return indexes[tool][species][build]


def _request(method, table, path, **kwargs):
    """Make a generic request with the Airtable API"""
    headers = {'Authorization': 'Bearer ' + AIRTABLE_API_KEY}
    url = API_ENDPOINT + table + path

    response = requests.request(method.upper(), url, headers=headers, **kwargs)
    response.raise_for_status()
    content = response.json()
    return content


def get_sample_by_key(key):
    """Retrieve Samples record by key from Airtable API"""
    return _request('get', 'Genomics%20Samples', '/' + key)


def get_sample(sample_id):
    """Retrieve Samples record by name from Airtable API"""
    params = {
        'filterByFormula': '{Name} = "%s"' % sample_id,
    }
    records = _request('get', 'Genomics%20Samples', '/', params=params)['records']
    return records[0]


def get_experiment_by_key(key):
    """Retrieve Experiment record by key from Airtable API"""
    return _request('get', 'Genomics%20Expts', '/' + key)


def get_experiment(expt_id):
    """Retrieve Experiment record by Name from Airtable API"""
    params = {
        'filterByFormula': '{Name} = "%s"' % expt_id,
    }
    return _request('get', 'Genomics%20Expts', '/', params=params)['records'][0]


class Sample(object):

    sample_id = Parameter()

    @property
    def sample(self):
        if not hasattr(self, '_sample'):
            self._sample = get_sample(self.sample_id)['fields']
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
            self._experiment = get_experiment_by_key(self.sample['Experiment'][0])['fields']
        return self._experiment



class FastQC(Task, Sample):

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

    def run(self):
        fq1, fq2 = [tgt.path for tgt in self.input()]
        out_dir = op.dirname(self.output()['html_1'].path) + '/'

        cmd = DOCKER_RUN + ['outlierbio/fastqc', fq1, fq2, out_dir, self.sample_id]
        run_logged(cmd)


class UpdateFastQC(Task, Sample):
    pass


class Star(Task, Sample):

    @property
    def prefix(self):        
        return 's3://{}/{}/star/{}'.format(
            S3_BUCKET, self.sample_folder, self.sample_id + '.')

    def requires(self):
        return (S3PathTask(path=self.sample['FastQ 1']),
                S3PathTask(path=self.sample['FastQ 2']))

    def output(self):
        s3_paths = {k: v.format(prefix=self.prefix) for k, v in STAR_OUTPUTS.items()}
        return {k: S3Target(path) for k, path in s3_paths.items()}

    def run(self):
        fq1, fq2 = [tgt.path for tgt in self.input()]

        cmd = DOCKER_RUN + [
            'outlierbio/star', 
            fq1, fq2, 
            get_index('star', build='test'), 
            self.prefix, 
            str(THREADS)
        ]
        run_logged(cmd)


class IndexBam(Task, Sample):

    def requires(self):
        return Star(sample_id=self.sample_id)

    def output(self):
        return self.input().path + '.bai'

    def run(self):
        cmd = DOCKER_RUN + [
            'outlierbio/samtools', 'index', 
            self.input()['bam'].path, 
            self.output().path
            ]

        run_logged(cmd)


class Kallisto(Task, Sample):

    def requires(self):
        return (S3PathTask(path=self.sample['FastQ 1']),
                S3PathTask(path=self.sample['FastQ 2']))

    def output(self):
        s3_paths = {
            'abundance': 'abundance.tsv',
            'h5': 'abundance.h5',
            'run_info': 'run_info.json'
        }
        return {k: S3Target('s3://{}/{}/kallisto/{}'.format(S3_BUCKET, self.sample_folder, fname))
                for k, fname in s3_paths.items()}

    def run(self):
        fq1, fq2 = [tgt.path for tgt in self.input()]
        out_dir = op.dirname(self.output()['abundance'].path) + '/'

        cmd = DOCKER_RUN + [
            'outlierbio/kallisto', 'quant',
            '-i', get_index('kallisto', build='test'), 
            '-o', out_dir,
            fq1, fq2
        ]
        run_logged(cmd)
        

class RnaSeq(WrapperTask):

    expt_id = Parameter()

    def requires(self):
        sample_keys = get_experiment(self.expt_id)['fields']['Genomics samples']

        for sample_key in sample_keys:
            sample = get_sample_by_key(sample_key)
            sample_id = sample['fields']['Name']

            yield FastQC(sample_id=sample_id)
            yield Star(sample_id=sample_id)
            yield Kallisto(sample_id=sample_id)



