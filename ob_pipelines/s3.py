from functools import wraps
import logging
import os
import os.path as op
from subprocess import check_output
import sys
from tempfile import mkstemp, mkdtemp
from urllib.parse import urlparse

import boto3
import botocore

logger = logging.getLogger('ob-pipelines')

s3 = boto3.client('s3')

SCRATCH_DIR = os.environ.get('SCRATCH_DIR') or '/tmp'


def path_to_bucket_and_key(path):
    (scheme, netloc, path, params, query, fragment) = urlparse(path)
    path_without_initial_slash = path[1:]
    return netloc, path_without_initial_slash


def download_folder(bucket, prefix, folder):
    response = s3.list_objects(
        Bucket=bucket, 
        Prefix=prefix,
        Delimiter='/'
    )
    if 'Contents' not in response and response['HTTPStatusCode'] == 200:
        raise botocore.exceptions.ClientError
    for key_dict in response['Contents']:
        key = key_dict['Key']
        fpath = op.join(folder, op.basename(key))
        s3.download_file(bucket, key, fpath)


def s3args(f):
    """Sync S3 path arguments with behind-the-scenes S3 transfers

    When decorating a function, s3args downloads all arguments that 
    look like S3 paths to temporary files and swaps the local temp
    filepath as the new argument. If the S3 path does not exist, it 
    is assumed to be an output, and s3args uploads the tempfile 
    back to S3 after the command is complete.

    This works great with Luigi, which checks for existence of inputs
    and non-existence of outputs before running a Task.

    Keyword args are passed directly without syncing, for now.
    """
    @wraps(f)
    def local_fn(*args, **kwargs):

        # Swap S3 paths in arguments with local paths
        # If the S3 path exists, it's an input, download first.
        # Otherwise, it's an output, save for upload after the command
        s3_outputs = {}
        local_args = []
        for arg in args:
            if not arg.startswith('s3://'):
                local_args.append(arg)
                continue
            
            src_bucket, src_key = path_to_bucket_and_key(arg)
            try:
                if src_key.endswith('/'):
                    # Download all files in folder
                    local_tmp = mkdtemp(prefix=op.basename(arg) + '_', dir=SCRATCH_DIR)
                    download_folder(src_bucket, src_key, local_tmp)
                else:
                    _, local_tmp = mkstemp(prefix=op.basename(arg) + '_', dir=SCRATCH_DIR)
                    s3.download_file(src_bucket, src_key, local_tmp)
            # TODO check for specifically key not found errors
            except botocore.exceptions.ClientError as e:
                s3_outputs[arg] = local_tmp
            local_args.append(local_tmp)

        # Run command and save output
        out = f(*local_args, **kwargs)

        # Upload outputs
        for s3_path, local_path in s3_outputs.items():
            dst_bucket, dst_key = path_to_bucket_and_key(s3_path)
            s3.upload_file(local_path, dst_bucket, dst_key)

        return out

    return local_fn


@s3args
def sync_and_run(*cmds):
    logger.info('Running:\n{}'.format(' '.join(cmds)))
    check_output(cmds)


def s3wrap():
    args = sys.argv[1:]
    sync_and_run(*args)
