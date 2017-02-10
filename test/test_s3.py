import os
import os.path as op
import shutil
from subprocess import check_output
from tempfile import mkstemp, mkdtemp
import boto3
import pytest

from ob_pipelines.s3 import (
    s3args, key_exists, path_to_bucket_and_key, create_tmp_from_key,
    upload_folder, download_folder, swap_args
)

TEST_BUCKET = os.environ.get('TEST_BUCKET')
OUT_KEY = 'test_out'
IN_KEY = 'test_in'
IN_PREFIX = 'test_prefix/'
OUT_PREFIX = 'test_out_prefix/'
s3 = boto3.client('s3')


@pytest.fixture
def s3_outpath():
    s3.delete_object(Bucket=TEST_BUCKET, Key=OUT_KEY)
    return 's3://{}/{}'.format(TEST_BUCKET, OUT_KEY)


@pytest.fixture
def s3_inpath():
    s3.put_object(Body=b'testing', Bucket=TEST_BUCKET, Key=IN_KEY)
    return 's3://{}/{}'.format(TEST_BUCKET, IN_KEY)


@pytest.fixture
def s3_infolder():
    for i in range(3):
        s3.put_object(Body=b'testing', Bucket=TEST_BUCKET, Key=IN_PREFIX + str(i))
    return 's3://{}/{}'.format(TEST_BUCKET, IN_PREFIX)


@pytest.fixture
def s3_outfolder():
    for i in range(3):
        s3.put_object(Body=b'testing', Bucket=TEST_BUCKET, Key=IN_PREFIX + str(i))
    return 's3://{}/{}'.format(TEST_BUCKET, IN_PREFIX)


def test_path_to_bucket_and_key():
    bucket, key = path_to_bucket_and_key('s3://bucket/key')
    assert bucket == 'bucket'
    assert key == 'key'

    bucket, key = path_to_bucket_and_key('s3://bucket/key/')
    assert key == 'key/'

    bucket, key = path_to_bucket_and_key('s3://bucket/path/to/key')
    assert key == 'path/to/key'


def test_create_tmp_from_key():
    tmp = create_tmp_from_key('file.ext')
    assert tmp.endswith('.ext')
    assert op.exists(tmp)
    assert op.isfile(tmp)
    os.remove(tmp)

    tmp = create_tmp_from_key('folder/')
    assert op.exists(tmp)
    assert op.isdir(tmp)
    assert 'folder' in tmp
    shutil.rmtree(tmp)


def test_key_exists(s3_inpath, s3_infolder):
    bucket, key = path_to_bucket_and_key(s3_inpath)
    assert key_exists(bucket, key)
    assert not key_exists(bucket, 'notakey')

    bucket, key = path_to_bucket_and_key(s3_infolder)
    assert key_exists(bucket, key)


def test_download_folder(s3_infolder):
    local_folder = mkdtemp()
    bucket, prefix = path_to_bucket_and_key(s3_infolder)
    download_folder(bucket, prefix, local_folder)
    assert op.exists(op.join(local_folder, '0'))
    assert op.exists(op.join(local_folder, '1'))
    assert op.exists(op.join(local_folder, '2'))


def test_upload_folder(s3_outfolder):
    local_folder = mkdtemp()
    for i in range(3):
        with open(op.join(local_folder, str(i)), 'w') as fw:
            fw.write('testing')
    upload_folder(local_folder, TEST_BUCKET, OUT_PREFIX)
    assert key_exists(TEST_BUCKET, OUT_PREFIX + '0')
    assert key_exists(TEST_BUCKET, OUT_PREFIX + '1')
    assert key_exists(TEST_BUCKET, OUT_PREFIX + '2')


def test_swap_args(s3_inpath):
    args = ['--param', 'arg', '/fpath/arg', 's3://nonexistent/s3/key', s3_inpath]
    local_args, s3_downloads, s3_uploads = swap_args(args)
    assert len(local_args) == len(args)
    assert 'arg' in local_args
    assert '/fpath/arg' in local_args
    assert 's3://nonexistent/s3/key' not in local_args
    assert s3_inpath not in local_args
    
    tmp_path_args = [arg for arg in local_args if arg.startswith('/tmp')]
    assert len(tmp_path_args) == 2
    assert 's3://nonexistent/s3/key' in s3_uploads
    assert s3_inpath in s3_downloads


def test_local_fn_run_unaltered():
    @s3args()
    def echo(arg1, arg2):
        return check_output(['echo', arg1, arg2])
    
    out = echo('hello', 'world')
    assert out == b'hello world\n'


@pytest.mark.skipif(TEST_BUCKET is None, reason='Need an accessible S3 bucket')
def test_upload_s3_s3args(s3_outpath):
    @s3args()
    def write_message(arg1, arg2):
        out = check_output(['echo', arg1])
        with open(arg2, 'w') as fw:
            fw.write(out.decode())

    write_message('test', s3_outpath)
    assert s3.get_object(Bucket=TEST_BUCKET, Key=OUT_KEY)['Body'].read() == b'test\n'


@pytest.mark.skipif(TEST_BUCKET is None, reason='Need an accessible S3 bucket')
def test_download_file_s3args(s3_inpath):
    @s3args()
    def cat_message(arg1, arg2):
        with open(arg2) as f:
            msg = f.read().strip()
        return check_output(['echo', arg1, msg])

    out = cat_message('just', s3_inpath)
    assert out == b'just testing\n'


@pytest.mark.skipif(TEST_BUCKET is None, reason='Need an accessible S3 bucket')
def test_download_folder_s3args(s3_infolder):
    @s3args()
    def cat_message(msg, folder):
        files = os.listdir(folder)
        for fpath in files:
            with open(op.join(folder, fpath)) as f:
                msg += ' ' + f.read().strip()
        return check_output(['echo', msg])

    out = cat_message('just', s3_infolder)
    assert out == b'just testing testing testing\n'