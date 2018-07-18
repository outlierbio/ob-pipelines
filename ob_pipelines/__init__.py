import logging
import os
import traceback
from datetime import datetime

import luigi
from mongoengine import connect

import ob_pipelines
from ob_pipelines.batch import JobTask
from ob_pipelines.config import settings
from ob_pipelines.entities import Job, Task

logger = logging.getLogger(__name__)

# Create the format
formatter = logging.Formatter('%(asctime)s - %(message)s')

# Add a console handler
ch = logging.StreamHandler()
ch.setLevel(os.environ.get('LOGGING_LEVEL') or logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

connect(host=settings.db_connection)


@JobTask.event_handler(luigi.event.Event.START)
def luigi_task_start(task: JobTask):
    job = Job.objects.get(id=task.job_id)
    db_task: Task = Task(job=job, name=task.get_task_family(), started_at=datetime.now())
    db_task.save()
    task.db_task_id = db_task.id


@JobTask.event_handler(luigi.event.Event.SUCCESS)
def luigi_task_success(task: JobTask):
    db_task: Task = Task.objects.get(id=task.db_task_id)
    db_task.completed_at = datetime.now()
    db_task.save()


@JobTask.event_handler(luigi.event.Event.FAILURE)
def luigi_task_failure(task: JobTask, exc):
    db_task: Task = Task.objects.get(id=task.db_task_id)
    db_task.completed_at = datetime.now()
    db_task.exception = traceback.format_exc()
    db_task.save()