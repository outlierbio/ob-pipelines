import os
from subprocess import check_output
import boto3
import pytest

from ob_pipelines.s3 import s3args

TEST_BUCKET = os.environ.get('TEST_BUCKET')
OUT_KEY = 'test_out'
IN_KEY = 'test_in'
s3 = boto3.client('s3')


@pytest.fixture
def s3_outpath():
    s3.delete_object(Bucket=TEST_BUCKET, Key=OUT_KEY)
    return 's3://{}/{}'.format(TEST_BUCKET, OUT_KEY)


@pytest.fixture
def s3_inpath():
    s3.put_object(Body=b'testing', Bucket=TEST_BUCKET, Key=IN_KEY)
    return 's3://{}/{}'.format(TEST_BUCKET, IN_KEY)


def test_local_fn_run_unaltered():

    @s3args
    def echo(arg1, arg2):
        return check_output(['echo', arg1, arg2])
    
    out = echo('hello', 'world')
    assert out == b'hello world\n'


@pytest.mark.skipif(TEST_BUCKET is None, reason='Need an accessible S3 bucket')
def test_upload_s3(s3_outpath):

    @s3args
    def write_message(arg1, arg2):
        out = check_output(['echo', arg1])
        with open(arg2, 'w') as fw:
            fw.write(out.decode())

    write_message('test', s3_outpath)
    assert s3.get_object(Bucket=TEST_BUCKET, Key=OUT_KEY)['Body'].read() == b'test\n'


@pytest.mark.skipif(TEST_BUCKET is None, reason='Need an accessible S3 bucket')
def test_download_s3(s3_inpath):

    @s3args
    def cat_message(arg1, arg2):
        with open(arg2) as f:
            msg = f.read().strip()
        return check_output(['echo', arg1, msg])

    out = cat_message('just', s3_inpath)
    assert out == b'just testing\n'
