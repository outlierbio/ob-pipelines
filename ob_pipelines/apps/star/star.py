import os.path as op
import logging

import click

from ob_pipelines.s3 import sync_and_run, SCRATCH_DIR, s3, path_to_bucket_and_key

logger = logging.getLogger('ob-pipelines')


STAR_OUTPUTS = [
    '{prefix}Aligned.sortedByCoord.out.bam',
    '{prefix}SJ.out.tab',
    '{prefix}Unmapped.out.mate1',
    '{prefix}Unmapped.out.mate2',
    '{prefix}Log.final.out'
]

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
        local_prefix = op.join(SCRATCH_DIR, op.basename(prefix)) 
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
        '--outSAMtype', 'BAM', 'SortedByCoordinate',
        '--outBAMcompression', '6'
    ]
    print(' '.join(cmd))
    logging.info('Running:\n{}'.format(' '.join(cmd)))
    sync_and_run(*cmd)

    # Upload temp out directory to S3 with prefix
    if prefix.startswith('s3://'):
    	upload_prefix(local_prefix, prefix, STAR_OUTPUTS)


if __name__ == '__main__':
	align()
