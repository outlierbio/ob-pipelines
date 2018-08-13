import logging
import os
from datetime import datetime

import luigi

import ob_pipelines
from ob_pipelines.batch import LoggingTaskWrapper
from ob_pipelines.entities.persistence import create_task, get_task_by_key, update_task
from ob_pipelines.entities.task import Task

logger = logging.getLogger(__name__)

# Create the format
formatter = logging.Formatter('%(asctime)s - %(message)s')

# Add a console handler
ch = logging.StreamHandler()
ch.setLevel(os.environ.get('LOGGING_LEVEL') or logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


@LoggingTaskWrapper.event_handler(luigi.event.Event.START)
def luigi_task_start(luigi_task: LoggingTaskWrapper):
    task: Task = Task()
    task.name = luigi_task.task_id
    task.status = 'running'
    task.started_at = datetime.utcnow().isoformat()
    luigi_task.task_key = create_task(task).key


@LoggingTaskWrapper.event_handler(luigi.event.Event.SUCCESS)
def luigi_task_success(luigi_task: LoggingTaskWrapper):
    task = get_task_by_key(luigi_task.task_key)
    task.completed_at = datetime.utcnow().isoformat()
    task.status = 'completed'
    update_task(task)


@LoggingTaskWrapper.event_handler(luigi.event.Event.FAILURE)
def luigi_task_failure(luigi_task: LoggingTaskWrapper, exception):
    task = get_task_by_key(luigi_task.task_key)
    task.completed_at = datetime.utcnow().isoformat()
    task.status = 'failed'
    task.exception = str(exception)
    update_task(task)
