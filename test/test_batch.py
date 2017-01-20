"""
Integration test for the Luigi wrapper of AWS Batch

Requires:

- boto3 package
- Amazon AWS credentials discoverable by boto3 (e.g., by using ``aws configure``
from awscli_)
- An enabled AWS Batch job queue configured to run on a compute environment.

Written and maintained by Jake Feala (@jfeala) for Outlier Bio (@outlierbio)

"""

import unittest

try:
    from ob_pipelines.batch import BatchTask, BatchJobException, client, _get_job_status
except ImportError:
    raise unittest.SkipTest('boto3 is not installed. BatchTasks require boto3')



TEST_JOB_DEF = {
    'jobDefinitionName': 'hello-world',
    'type': 'container',
    'parameters': {
        'message': 'hll wrld'
    },
    'containerProperties': {
        'image': 'centos',
        'command': ['/bin/echo', 'Ref::message'],
        'vcpus': 2,
        'memory': 4,
    }
}


class BatchTaskNoOutput(BatchTask):

    def complete(self):
        if self.batch_job_id:
            return _get_job_status(self.batch_job_id) == 'SUCCEEDED'
        return False


class BatchTaskOverrideCommand(BatchTaskNoOutput):

    @property
    def command(self):
        return ['/bin/sleep', '10']


class BatchTaskOverrideFailingCommand(BatchTaskNoOutput):

    @property
    def command(self):
        return ['not', 'a', 'command']


class BatchTaskNonzeroExitCommand(BatchTaskNoOutput):

    @property
    def command(self):
        return ['exit', '1']


class TestBatchTask(unittest.TestCase):

    def setUp(self):
        # Register the test task definition
        response = client.register_job_definition(**TEST_JOB_DEF)
        self.arn = response['jobDefinitionArn']

    def test_unregistered_task(self):
        t = BatchTaskNoOutput(job_def=TEST_JOB_DEF, job_name='test_unregistered')
        t.run()

    def test_registered_task(self):
        t = BatchTaskNoOutput(job_def_arn=self.arn, job_name='test_registered')
        t.run()

    def test_override_command(self):
        t = BatchTaskOverrideCommand(job_def_arn=self.arn, job_name='test_override')
        t.run()

    def test_failing_command(self):
        t = BatchTaskOverrideFailingCommand(job_def_arn=self.arn, job_name='test_failure')
        with self.assertRaises(BatchJobException):
            t.run()

    def test_nonzero_exit(self):
        t = BatchTaskNonzeroExitCommand(job_def_arn=self.arn, job_name='test_nonzero_exit')
        with self.assertRaises(BatchJobException):
            t.run()
