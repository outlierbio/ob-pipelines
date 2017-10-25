import os.path as op
import logging
import shutil
from subprocess import check_output
from tempfile import mkdtemp

import click

from ob_pipelines.s3 import (
    swap_args, download_file_or_folder, remove_file_or_folder, SCRATCH_DIR, s3, path_to_bucket_and_key
)

logger = logging.getLogger('ob-pipelines')


STAR_OUTPUTS = {
    'bam': '{prefix}Aligned.out.bam',
    'junctions': '{prefix}SJ.out.tab',
    'unmapped_1': '{prefix}Unmapped.out.mate1',
    'unmapped_2': '{prefix}Unmapped.out.mate2',
    'log': '{prefix}Log.final.out'
}


def upload_prefix(local_prefix, s3_prefix, fpath_templates):
    """Upload all files matching a template to S3"""
    local_fpaths = [fpath.format(prefix=local_prefix) for fpath in fpath_templates]
    s3_fpaths = [fpath.format(prefix=s3_prefix) for fpath in fpath_templates]
    for local_fpath, s3_fpath in zip(local_fpaths, s3_fpaths):
        bucket, key = path_to_bucket_and_key(s3_fpath)
        s3.upload_file(local_fpath, bucket, key)


@click.command()
@click.argument('fq1')
@click.argument('fq2')
@click.argument('genome_dir')
@click.argument('prefix')
@click.argument('threads')
def align(fq1, fq2, genome_dir, prefix, threads):
    """STAR RNA-seq aligner"""

    # Output prefixes are messy and the s3args wrapper can't handle them
    # yet, so we have to manage the transfer of outputs here.
    if prefix.startswith('s3://'):
        tmp_dir = mkdtemp(
            prefix='star_', 
            dir=SCRATCH_DIR)
        local_prefix = op.join(tmp_dir, op.basename(prefix)) 
    else: 
        local_prefix = prefix

    # Not required by STAR, but trailing slash lets S3 magic know it's a directory
    if genome_dir.startswith('s3://') and not genome_dir.endswith('/'):
    	genome_dir += '/'

    cmd = [
        'STAR',
        '--genomeDir', genome_dir,
        '--runThreadN', str(threads),
        '--readFilesIn', fq1, fq2,
        '--readFilesCommand', 'zcat',
        '--outFileNamePrefix', local_prefix,
        '--outReadsUnmapped', 'Fastx',
        '--outSAMattributes', 'All',
        '--outSAMstrandField', 'intronMotif',
        '--outSAMtype', 'BAM', 'Unsorted',
        '--outBAMcompression', '6'
    ]

    # Swap the S3 path arguments for local temporary files/folders
    local_args, s3_downloads, _ = swap_args(cmd)

    try:
        # Download inputs
        logging.info('syncing from S3')
        for s3_path, local_path in s3_downloads.items():
            download_file_or_folder(s3_path, local_path)

        # Run command and save output
        logging.info('Running:\n{}'.format(' '.join(cmd)))
        out = check_output(local_args)
        logging.info(out.decode())

        # Upload temp out directory to S3 with prefix
        if prefix.startswith('s3://'):
            upload_prefix(local_prefix, prefix, STAR_OUTPUTS.values())
    finally:
        if prefix.startswith('s3://'):
            shutil.rmtree(tmp_dir)
        for local_path in s3_downloads.values():
            remove_file_or_folder(local_path)


if __name__ == '__main__':
    align()
