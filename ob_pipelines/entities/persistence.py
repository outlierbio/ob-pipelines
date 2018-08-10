from ob_airtable import AirtableClient

from ob_pipelines.config import cfg
from ob_pipelines.entities.experiment import Experiment
from ob_pipelines.entities.sample import Sample
from ob_pipelines.entities.task import Task

ENDPOINT = cfg['AIRTABLE_API_ENDPOINT']
API_KEY = cfg['AIRTABLE_API_KEY']
EXPT_TABLE = cfg['AIRTABLE_EXPT_TABLE']
SAMPLE_TABLE = cfg['AIRTABLE_SAMPLE_TABLE']
TASK_TABLE = cfg['AIRTABLE_TASK_TABLE']

_client = AirtableClient(endpoint=ENDPOINT, api_key=API_KEY)


def _get_record(key, table):
    return _client.get_record(key, table)


def _get_records(table):
    return _client.get_records(table)


def _get_record_by_name(name, table):
    return _client.get_record_by_name(name, table)


def get_samples_by_experiment_id(expt_id):
    expt = get_experiment_by_name(expt_id)

    for sample_key in expt.Samples:
        sample = get_sample_by_key(sample_key)
        yield sample.sample['Name']


def get_experiment_by_name(expt_name):
    return Experiment(**_get_record_by_name(expt_name, EXPT_TABLE))


def get_sample_by_name(sample_name):
    sample = Sample(**_get_record_by_name(sample_name, SAMPLE_TABLE))
    sample.experiment = get_experiment_by_key(sample.sample['Experiment'][0])
    return sample


def get_task_by_name(task_name):
    return Task(**_get_record_by_name(task_name, TASK_TABLE))


def get_experiment_by_key(expt_key):
    return Experiment(**_get_record(expt_key, EXPT_TABLE))


def get_sample_by_key(sample_key):
    sample = Sample(**_get_record(sample_key, SAMPLE_TABLE))
    sample.experiment = get_experiment_by_key(sample.sample['Experiment'][0])
    return sample


def get_task_by_key(task_key):
    return Task(**_get_record(task_key, TASK_TABLE))


def get_samples():
    samples = _get_records(SAMPLE_TABLE)
    for sample in samples:
        yield Sample(**sample)


def get_experiments() -> []:
    experiments = _get_records(EXPT_TABLE)
    for experiment in experiments:
        yield Experiment(**experiment)


def get_tasks():
    tasks = _get_records(TASK_TABLE)
    for task in tasks:
        yield Task(**task)


def create_task(task: Task):
    entity = {'Name': task.name, 'Exception': task.exception, 'Status': task.status,
              'Started_at': task.started_at}
    return Task(**_client.create_record(entity, TASK_TABLE))


def update_task(task: Task):
    entity = {'fields': {'Name': task.name, 'Status': task.status, 'Exception': task.exception,
                         'Completed_at': task.completed_at, 'Started_at': task.started_at}}
    return _client.update_record(task.key, TASK_TABLE, entity)
