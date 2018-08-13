import luigi
from luigi.contrib.s3 import S3Target

from ob_pipelines.batch import BatchTask, LoggingTaskWrapper


class GDCDownload(BatchTask, LoggingTaskWrapper):

    """Download from GDC on AWS Batch"""

    download_id =  luigi.Parameter()
    manifest = luigi.Parameter()
    outpath = luigi.Parameter()
    token = luigi.Parameter()
    job_definition = 'gdc'

    @property
    def job_name(self):
        return '{}-gdc-download-manifest'.format(self.download_id)

    @property
    def parameters(self):
        return {
            'download_id': self.download_id,
            'manifest': self.manifest,
            'outpath': self.outpath if str(self.outpath).endswith('/') else self.outpath + '/',
            'token': self.token
        }

    def output(self):
        s3_path = '{folder}/{download_id}'
        return S3Target(s3_path.format(folder=self.outpath, download_id=self.download_id))