import os.path as op
from subprocess import check_output
import logging

import click

from ob_pipelines.s3 import s3args, SCRATCH_DIR, s3, path_to_bucket_and_key

logger = logging.getLogger('ob-pipelines')


STAR_OUTPUTS = [
    '{prefix}.Aligned.out.bam',
    '{prefix}.SJ.out.tab',
    '{prefix}.Unmapped.out.mate1',
    '{prefix}.Unmapped.out.mate2',
    '{prefix}.Log.final.out'
]


@s3args
def _sync_and_run(*cmds):
    check_output(cmds)


@click.command
@click.argument('fq1')
@click.argument('fq2')
@click.argument('genome_dir')
@click.argument('prefix')
@click.argument('threads')
def align(fq1, fq2, genome_dir, prefix, threads):
    """STAR RNA-seq aligner"""

    if prefix.startswith('s3://'):
        local_prefix = op.join(SCRATCH_DIR, op.basename(prefix)) 
    else: 
        local_prefix = prefix

    cmd = [
        'STAR',
        '--genomeDir', genome_dir,
        '--runThreadN', str(threads),
        '--outFileNamePrefix', local_prefix,
        '--outReadsUnmapped', 'Fastx',
        '--outSAMattributes', 'All',
        '--readFilesIn', fq1, fq2,
        '--outSAMstrandField', 'intronMotif',
        '--readFilesCommand', 'zcat'
    ]

    logging.info('Running:\n{}'.format(' '.join(cmd)))
    _sync_and_run(cmd)

    if prefix.startwith('s3://'):
        local_fpaths = [fpath.format(local_prefix) for fpath in STAR_OUTPUTS]
        s3_fpaths = [fpath.format(local_prefix) for fpath in STAR_OUTPUTS]
        for local_fpath, s3_fpath in zip(local_fpaths, s3_fpaths):
            bucket, key = path_to_bucket_and_key(s3_fpath)
            s3.upload_file(local_fpath, bucket, key)


if __name__ == '__main__':
    align()
