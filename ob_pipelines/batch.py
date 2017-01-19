"""
AWS Batch wrapper for Luigi

From the AWS website:

    AWS Batch enables you to run batch computing workloads on the AWS Cloud. 

    Batch computing is a common way for developers, scientists, and engineers 
    to access large amounts of compute resources, and AWS Batch removes the 
    undifferentiated heavy lifting of configuring and managing the required 
    infrastructure. AWS Batch is similar to traditional batch computing 
    software. This service can efficiently provision resources in response to 
    jobs submitted in order to eliminate capacity constraints, reduce compute 
    costs, and deliver results quickly.

See `AWS Batch User Guide`_ for more details.

To use AWS Batch, you create a jobDefinition JSON that defines a `docker run`_
command, and then submit this JSON to the API to queue up the task. Behind the
scenes, AWS Batch auto-scales a fleet of EC2 Container Service instances, 
monitors the load on these instances, and schedules the jobs.

This `boto3-powered`_ wrapper allows you to create Luigi Tasks to submit Batch
``jobDefinition`` s. You can either pass a dict (mapping directly to the
``jobDefinition`` JSON) OR an Amazon Resource Name (arn) for a previously
registered ``jobDefinition``.

Requires:

- boto3 package
- Amazon AWS credentials discoverable by boto3 (e.g., by using ``aws configure``
  from awscli_)
- An enabled AWS Batch job queue configured to run on a compute environment.

Written and maintained by Jake Feala (@jfeala) for Outlier Bio (@outlierbio)

.. _`docker run`: https://docs.docker.com/reference/commandline/run
.. _jobDefinition: http://http://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html
.. _`boto3-powered`: https://boto3.readthedocs.io
.. _awscli: https://aws.amazon.com/cli
.. _`AWS Batch User Guide`: http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_GetStarted.html

"""

import json
import os
import logging
import random
import string
import time

import luigi

logger = logging.getLogger('luigi-interface')

try:
    import boto3
    client = boto3.client('batch')

    # Get dict of active queues keyed by name
    queues = {q['jobQueueName']:q for q in client.describe_job_queues()['jobQueues']
              if q['state'] == 'ENABLED' and q['status'] == 'VALID'}
    if not queues:
        logger.warning('No job queues with state=ENABLED and status=VALID')

    # Allow queue to be specified as env var, or just pick the first one
    queue_name = list(queues.keys())[0] or os.environ.get('BATCH_QUEUE_NAME')

    # Get queue to submit jobs
    queue = queues[queue_name]
except ImportError:
    logger.warning('boto3 is not installed. BatchTasks require boto3')

class BatchJobException(Exception):
    pass

POLL_TIME = 2


def random_id():
    return 'luigi-job-' + ''.join(random.sample(string.ascii_lowercase, 8))


def _get_job_status(job_id):
    """
    Retrieve task statuses from ECS API

    Returns list of {SUBMITTED|PENDING|RUNNABLE|STARTING|RUNNING|SUCCEEDED|FAILED} for each id in job_ids
    """
    response = client.describe_jobs(jobs=[job_id])

    # Error checking
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code != 200:
        msg = 'Job status request received status code {0}:\n{1}'
        raise Exception(msg.format(status_code, response))

    return response['jobs'][0]['status']

def _track_job(job_id):
    """Poll task status until STOPPED"""
    
    while True:
        status = _get_job_status(job_id)
        if status in ['SUCCEEDED', 'FAILED']:
            logger.info('Batch job {0} finished'.format(job_id))
            return status

        time.sleep(POLL_TIME)
        logger.debug('Batch job status for job {0}: {1}'.format(
            job_id, status))


class BatchTask(luigi.Task):

    """
    Base class for an Amazon Batch job

    Amazon Batch requires you to register "jobs", which are JSON descriptions
    for how to issue the ``docker run`` command. This Luigi Task can either
    run a pre-registered Batch jobDefinition, OR you can register the job on 
    the fly from a Python dict.

    :param job_def_arn: pre-registered job definition ARN (Amazon Resource
        Name), of the form::

            arn:aws:batch:<region>:<user_id>:job-definition/<job-name>:<version>

    :param job_def: dict describing job in jobDefinition JSON format, for
        example::

            job_def = {
                'family': 'hello-world',
                'volumes': [],
                'containerDefinitions': [
                    {
                        'memory': 1,
                        'essential': True,
                        'name': 'hello-world',
                        'image': 'ubuntu',
                        'command': ['/bin/echo', 'hello world']
                    }
                ]
            }

    """

    job_name = luigi.Parameter(default='')
    job_def_arn = luigi.Parameter(default='')
    job_def = luigi.DictParameter(default={})
    vcpus = luigi.IntParameter(default=1)
    memory = luigi.IntParameter(default=4)

    @property
    def parameters(self):
        """
        Parameters to pass to the command template

        Override to return a dict of key-value pairs to fill in command arguments
        """
        return {}

    @property
    def environment(self):
        """
        Environment variables to pass to the container

        Override to return a list of dicts with keys 'name' and 'value', for 
        passing environment variables. For example::

            return [{'name': 'foo', 'value': 'bar'}]

        """
        return []

    @property
    def command(self):
        """
        Command passed to the containers

        Override to return list of strings describing new command to override
        Docker CMD within the container. Use "Ref::param_name" for template parameters
        that can be filled dynamically with self.parameters. For example::

            return ['/bin/sleep', 'Ref::duration']

        In this case, you would want self.parameters to return {'duration': <int>}

        """
        return []

    @property
    def batch_job_id(self):
        """Expose the Batch job ID"""
        if hasattr(self, '_job_id'):
            return self._job_id

    def run(self):
        if (not self.job_def and not self.job_def_arn) or \
           (self.job_def and self.job_def_arn):
            raise ValueError(('Either (but not both) a job_def (dict) or'
                              'job_def_arn (string) must be assigned'))
        if not self.job_def_arn:
            # Register the job and get assigned jobDefinition ID (arn)
            response = client.register_job_definition(**self.job_def)
            self.job_def_arn = response['jobDefinitionArn']

        # Add custom command to job
        overrides = {
            'vcpus': self.vcpus,
            'memory': self.memory,
            'command': self.command,
            'environment': self.environment,
        }

        # Submit the job to AWS Batch and get assigned job ID
        # (list containing 1 string)
        response = client.submit_job(
            jobName = self.job_name or random_id(),
            jobQueue = queue['jobQueueArn'],
            jobDefinition = self.job_def_arn,
            parameters = self.parameters,
            containerOverrides=overrides)
        self._job_id = response['jobId']

        # Wait on job completion
        status = _track_job(self._job_id)

        # Raise and notify if job failed
        if status == 'FAILED':
            data = client.describe_jobs(jobs=[self._job_id])['jobs']
            raise BatchJobException('Job {}: {}'.format(self._job_id, json.dumps(data, indent=4)))

