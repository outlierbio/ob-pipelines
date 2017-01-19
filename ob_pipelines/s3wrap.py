import logging
import os
import os.path as op
from tempfile import mkstemp
from subprocess import check_output

import boto3
import botocore
import click

logger = logging.getLogger('ob-pipelines')
s3 = boto3.resource('s3')

SCRATCH_DIR = os.environ.get('SCRATCH_DIR') or '/tmp'

def copy_s3(src, dst):
    cmd = 'aws s3 cp {src} {dst}'.format(src=src, dst=dst)
    logger.info('Running ' + cmd)
    check_output(cmd, shell=True)
    # or 
    # s3 = boto3.client('s3')
    # s3.upload_file("tmp.txt", "bucket-name", "key-name")

@click.command()
@click.argument('args', nargs=-1)
def s3wrap(args):

    # Swap S3 paths in arguments with local paths
    # If the S3 path exists, it's an input, download first.
    # Otherwise, it's an output, save for upload after the command
    s3_outputs = {}
    local_args = []
    for arg in enumerate(args):
        if arg.startswith('s3://'):
            _, local_tmp = mkstemp(prefix=op.basename(arg), dir=SCRATCH_DIR)
            try:
                copy_s3(arg, local_tmp)
            except botocore.exceptions.ClientError as e:
                # File not there, must be an output
                s3_outputs[arg] = local_tmp
            local_args.append(local_tmp)
        else:
            local_args.append(arg)

    # Run command with local args
    out, err = check_output(local_args)
    logger.info(out)
    logger.debug(err)

    for s3_path, local_path in s3_outputs.items():
        copy_s3(local_path, s3_path)


if __name__ == '__main__':
    s3wrap()
