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
import logging
import random
import string
import time

import luigi

logger = logging.getLogger(__name__)

try:
    import boto3
except ImportError:
    logger.warning('boto3 is not installed. BatchTasks require boto3')


class BatchJobException(Exception):
    pass


POLL_TIME = 10


def _random_id():
    return 'batch-job-' + ''.join(random.sample(string.ascii_lowercase, 8))


class BatchClient(object):

    def __init__(self):
        self._client = boto3.client('batch')
        self._queue = self.get_active_queue()

    def get_active_queue(self):
        """Get name of first active job queue"""
        # Get dict of active queues keyed by name
        queues = {q['jobQueueName']: q for q in self._client.describe_job_queues()['jobQueues']
                  if q['state'] == 'ENABLED' and q['status'] == 'VALID'}
        if not queues:
            raise Exception('No job queues with state=ENABLED and status=VALID')

        # Pick the first queue as default
        return list(queues.keys())[0]

    def get_job_id_from_name(self, job_name):
        # Job name is unique. If the job exists, use its id
        jobs = self._client.list_jobs(jobQueue=self._queue, jobStatus='RUNNING')['jobSummaryList']
        matching_jobs = [job for job in jobs if job['jobName'] == job_name]
        if matching_jobs:
            return matching_jobs[0]['jobId']

    def get_job_status(self, job_id):
        """
        Retrieve task statuses from ECS API

        Returns list of {SUBMITTED|PENDING|RUNNABLE|STARTING|RUNNING|SUCCEEDED|FAILED} for each id in job_ids
        """
        response = self._client.describe_jobs(jobs=[job_id])

        # Error checking
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code != 200:
            msg = 'Job status request received status code {0}:\n{1}'
            raise Exception(msg.format(status_code, response))

        return response['jobs'][0]['status']

    def submit_job(self, job_definition, parameters, job_name=None, queue=None):
        # Use boto3 client directly since it's easy
        if job_name is None:
            job_name = _random_id()
        response = self._client.submit_job(
            jobName=job_name,
            jobQueue=queue or self.get_active_queue(),
            jobDefinition=job_definition,
            parameters=parameters
        )
        return response['jobId']

    def wait_on_job(self, job_id):
        """Poll task status until STOPPED"""

        while True:
            status = self.get_job_status(job_id)
            if status == 'SUCCEEDED':
                logger.info('Batch job {} SUCCEEDED'.format(job_id))
                return True
            elif status == 'FAILED':
                # Raise and notify if job failed
                data = self._client.describe_jobs(jobs=[job_id])['jobs']
                raise BatchJobException('Job {} failed: {}'.format(job_id, json.dumps(data, indent=4)))

            time.sleep(POLL_TIME)
            logger.debug('Batch job status for job {0}: {1}'.format(
                job_id, status))

    def register_job_definition(self, json_fpath):
        """Register a job definition with AWS Batch, using a JSON"""
        with open(json_fpath) as f:
            job_def = json.load(f)
        response = self._client.register_job_definition(**job_def)
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code != 200:
            msg = 'Register job definition request received status code {0}:\n{1}'
            raise Exception(msg.format(status_code, response))
        return response


class BatchTask(luigi.Task):
    """
    Base class for an Amazon Batch job

    Amazon Batch requires you to register "jobs", which are JSON descriptions
    for how to issue the ``docker run`` command. This Luigi Task can either
    run a pre-registered Batch jobDefinition, OR you can register the job on 
    the fly from a Python dict.

    :param job_definition: pre-registered job definition ARN (Amazon Resource
        Name), of the form::

            arn:aws:batch:<region>:<user_id>:job-definition/<job-name>:<version>

    """
    job_name = None

    def run(self):
        bc = BatchClient()
        job_id = bc.submit_job(self.job_definition, self.parameters,
                               job_name=self.job_name)
        bc.wait_on_job(job_id)


class LoggingTaskWrapper(luigi.Task):

    @property
    def priority(self):
        return 50

    @property
    def task_key(self):
        return getattr(self, "__task_key", None)

    @task_key.setter
    def task_key(self, value):
        setattr(self, "__task_key", value)
