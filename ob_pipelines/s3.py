import argparse
from functools import wraps
from io import StringIO
import logging
import os
import os.path as op
import shutil
from subprocess import check_output
from tempfile import mkstemp, mkdtemp
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import boto3
import botocore

logger = logging.getLogger('ob-pipelines')

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')

SCRATCH_DIR = os.environ.get('SCRATCH_DIR') or '/tmp'


def csv_to_s3(df, s3_path):
    """Write pandas DataFrame to S3 object"""

    # Write dataframe to buffer
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)

    # Upload CSV to S3
    bucket, key = path_to_bucket_and_key(s3_path)
    s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())


def create_tmp_from_key(key): 
    """Create local temp file or folder depending on key path"""
    if key.endswith('/'):
        local_tmp = mkdtemp(
            prefix=op.basename(key.rstrip('/')) + '_', 
            dir=SCRATCH_DIR)
        local_tmp = local_tmp if local_tmp.endswith('/') else local_tmp + '/'
    else:
        fname = op.basename(key)
        base, ext = op.splitext(fname)
        _, local_tmp = mkstemp(prefix=base + '_',
                               suffix=ext,
                               dir=SCRATCH_DIR)
    return local_tmp


def path_to_bucket_and_key(path):
    (scheme, netloc, path, params, query, fragment) = urlparse(path)
    path_without_initial_slash = path[1:]
    return netloc, path_without_initial_slash


def key_exists(bucket, key):
    """Check for existence of S3 key"""
    try:
        if key.endswith('/'):
            return 'Contents' in s3.list_objects(Bucket=bucket, Prefix=key)
        else:
            s3_resource.Object(bucket, key).load()
            return True
    except botocore.exceptions.ClientError as e:
            return False


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


def upload_folder(folder, bucket, prefix):
    # Upload directory
    for fname in os.listdir(folder):
        fpath = op.join(folder, fname)
        key = prefix + fname
        s3.upload_file(fpath, bucket, key)


def download_file_or_folder(s3_path, local_path):
    """Dispatch S3 download depending on key path"""
    bucket, key = path_to_bucket_and_key(s3_path)
    if key.endswith('/'):
        download_folder(bucket, key, local_path)
    else:
        s3.download_file(bucket, key, local_path)
        if key.endswith('.bam'):
            # Always download a BAM index if it exists
            possible_index_keys = [key + '.bai', key.replace('.bam', '.bai')]
            for index_key in possible_index_keys:
                if key_exists(bucket, index_key):
                    s3.download_file(bucket, index_key, local_path + '.bai')



def upload_file_or_folder(s3_path, local_path):
    """Dispatch S3 upload depending on local path"""
    bucket, key = path_to_bucket_and_key(s3_path)
    if op.isfile(local_path):
        s3.upload_file(local_path, bucket, key)
    elif op.isdir(local_path):
        upload_folder(local_path, bucket, key)


def remove_file_or_folder(fpath):
    if op.isdir(fpath):
        shutil.rmtree(fpath)
    else:
        os.remove(fpath)


def swap_args(args, rm_local_outpath=False):
    """Swap S3 paths in arguments with local paths
    
    If the S3 path exists, it's an input, download first and swap the arg
    with a temporary filepath. Otherwise, it's an output, save for upload 
    after the command.

    Returns: 
        tuple of (local_args, s3_downloads, s3_uploads)

        where new_args contains the new argument list with local paths, 
        and s3_outputs is a dict mapping local filepaths to s3 paths to 
        transfer after execution.
    """
    s3_uploads = {}
    s3_downloads = {}
    local_args = []
    for arg in args:
        if not arg.startswith('s3://'):
            local_args.append(arg)
            continue
        
        src_bucket, src_key = path_to_bucket_and_key(arg)
        local_tmp = create_tmp_from_key(src_key)
        
        # If key exists, add path to downloads, otherwise add path to 
        # uploads and remove the file or folder
        if key_exists(src_bucket, src_key):
            s3_downloads[arg] = local_tmp
        else:
            s3_uploads[arg] = local_tmp
            if rm_local_outpath:
                remove_file_or_folder(local_tmp)

        local_args.append(local_tmp)

    return local_args, s3_downloads, s3_uploads


def s3args(rm_local_outpath=False):
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
    def s3args_decorator(f):
        @wraps(f)
        def local_fn(*args, **kwargs):

            # Swap the S3 path arguments for local temporary files/folders
            local_args, s3_downloads, s3_uploads = swap_args(args, rm_local_outpath=rm_local_outpath)

            # Download inputs
            logger.info('syncing from S3')
            for s3_path, local_path in s3_downloads.items():
                download_file_or_folder(s3_path, local_path)

            # Run command and save output
            out = f(*local_args, **kwargs)

            # Upload outputs
            logger.info('uploading to S3')
            for s3_path, local_path in s3_uploads.items():
                upload_file_or_folder(s3_path, local_path)

            # Remove local files
            local_paths = list(s3_downloads.values()) + list(s3_uploads.values())
            for local_path in local_paths:
                remove_file_or_folder(local_path)

            return out

        return local_fn
    return s3args_decorator


def s3wrap():
    parser = argparse.ArgumentParser(description='Swap S3 commands for temporary local paths and download')
    parser.add_argument('--rm-local-outpath', '-r', action='store_true', help='Remove local tmp output file/folder before executing command')
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    @s3args(rm_local_outpath=args.rm_local_outpath)
    def sync_and_run(*cmds):
        print('Running:\n{}'.format(' '.join(cmds)))
        return check_output(cmds)

    out = sync_and_run(*args.command) 
    print(out.decode())

