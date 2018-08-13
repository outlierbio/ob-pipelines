import logging
import os.path as op
import shutil
import subprocess
from tempfile import mkdtemp

import click

from ob_pipelines.s3 import (
    swap_args, upload_prefix, download_file_or_folder, remove_file_or_folder, SCRATCH_DIR
)

logger = logging.getLogger('__name__')

GENE_COVERAGE_OUTPUTS = {
    'png': '{prefix}.geneBodyCoverage.curves.png',
    'txt': '{prefix}.geneBodyCoverage.txt',
    'r': '{prefix}.geneBodyCoverage.r'
}


@click.command()
@click.argument('bam')
@click.argument('ref')
@click.argument('prefix')
def gene_coverage(bam, ref, prefix):
    """RSeQC gene body coverage"""

    # Output prefixes are messy and the s3args wrapper can't handle them
    # yet, so we have to manage the transfer of outputs here.
    if prefix.startswith('s3://'):
        tmp_dir = mkdtemp(
            prefix='rseqc_gbc_', 
            dir=SCRATCH_DIR)
        local_prefix = op.join(tmp_dir, op.basename(prefix)) 
    else: 
        local_prefix = prefix

    cmd = [
        "geneBody_coverage.py",
        "-f", "png",
        "-r", ref,
        "-i", bam,
        "-o", local_prefix
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
        try:
            out = subprocess.check_output(local_args, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
        except subprocess.CalledProcessError as exc:
            logging.info("Status : FAIL", exc.returncode, exc.output)
        else:
            logging.info(out)

        # Upload temp out directory to S3 with prefix
        if prefix.startswith('s3://'):
            upload_prefix(local_prefix, prefix, GENE_COVERAGE_OUTPUTS.values())
    finally:
        if prefix.startswith('s3://'):
            shutil.rmtree(tmp_dir)
        for local_path in s3_downloads.values():
            remove_file_or_folder(local_path)


if __name__ == '__main__':
    gene_coverage()
