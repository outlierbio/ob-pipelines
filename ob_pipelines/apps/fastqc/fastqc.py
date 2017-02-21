import os.path as op
import logging
import shutil
from subprocess import check_output
from tempfile import mkdtemp

import click

from ob_pipelines.s3 import (
    s3, download_file_or_folder, remove_file_or_folder, SCRATCH_DIR, path_to_bucket_and_key
)

logger = logging.getLogger('ob-pipelines')


@click.command()
@click.argument('fq1')
@click.argument('fq2')
@click.argument('out_dir')
@click.argument('name')
def fastqc(fq1, fq2, out_dir, name):
    """Run FastQC"""

    out_dir = out_dir if out_dir.endswith('/') else out_dir + '/'

    temp_dir = mkdtemp(dir=SCRATCH_DIR)
    fq1_local = op.join(temp_dir, name + '_1.fastq.gz')
    fq2_local = op.join(temp_dir, name + '_2.fastq.gz')

    if fq1.startswith('s3://'):
        # Assume that if fq1 is in S3, so is fq2
        download_file_or_folder(fq1, fq1_local)
        download_file_or_folder(fq2, fq2_local)
    else:
        shutil.copy(fq1, fq1_local)
        shutil.copy(fq2, fq2_local)

    cmd = ['fastqc', '-o', temp_dir, fq1_local, fq2_local]

    # Run command and save output
    logging.info('Running:\n{}'.format(' '.join(cmd)))
    out = check_output(cmd)
    logging.info(out.decode())

    out_files = [
        name + '_1_fastqc.html',
        name + '_2_fastqc.html',
        name + '_1_fastqc.zip',
        name + '_2_fastqc.zip'
    ]


    for fname in out_files:
        # Upload temp out directory to S3 with prefix
        if out_dir.startswith('s3://'):
            bucket, key = path_to_bucket_and_key(out_dir)
            local_fpath = op.join(temp_dir, fname)
            print('uploading {} to s3://{}/{}{}'.format(local_fpath, bucket, key, fname))
            s3.upload_file(local_fpath, bucket, key + fname)
            remove_file_or_folder(local_fpath)
        else:
            shutil.move(temp_dir, out_dir)


if __name__ == '__main__':
	fastqc()
