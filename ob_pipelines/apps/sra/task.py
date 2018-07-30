import luigi
from luigi.contrib.s3 import S3Target
from ob_pipelines.batch import BatchTask


class SRADownload(BatchTask):

    """Download from SRA on AWS Batch"""

    srr_id = luigi.Parameter()
    layout = luigi.Parameter(default='paired')
    outpath = luigi.Parameter()
    job_definition = 'sra'

    @property
    def job_name(self):
        return '{}-sra-download'.format(self.srr_id)

    @property
    def parameters(self):
        return {
            'srr_id': self.srr_id,
            'layout': self.layout,
            'outpath': self.outpath if str(self.outpath).endswith('/') else self.outpath + '/'
        }

    def output(self):
        if self.layout == 'paired':
            s3_path = '{folder}/{srr_id}_{pe}.fastq.gz'
            return {
                'fq1': S3Target(s3_path.format(
                    folder=self.outpath, pe=1, srr_id=self.srr_id)),
                'fq2': S3Target(s3_path.format(
                    folder=self.outpath, pe=2, srr_id=self.srr_id))
            }
        else:
            s3_path = '{folder}/{srr_id}.fastq.gz'
            return S3Target(s3_path.format(
                folder=self.outpath, srr_id=self.srr_id))