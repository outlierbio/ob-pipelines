import os

from luigi import Parameter
from ob_airtable import AirtableClient

from ob_pipelines.config import cfg

client = AirtableClient(endpoint=cfg['AIRTABLE_API_ENDPOINT'], api_key=cfg['AIRTABLE_API_KEY'])

def get_samples(expt_id):
    expt = client.get_record_by_name(expt_id, cfg['AIRTABLE_EXPT_TABLE'])
    sample_keys = expt['fields']['Genomics samples']

    for sample_key in sample_keys:
        sample = client.get_record(sample_key, cfg['AIRTABLE_SAMPLE_TABLE'])
        yield sample['fields']['Name']


class Sample(object):

    sample_id = Parameter()

    @property
    def sample(self):
        if not hasattr(self, '_sample'):
            self._sample = client.get_record_by_name(self.sample_id, cfg['AIRTABLE_SAMPLE_TABLE'])['fields']
        return self._sample

    @property
    def sample_folder(self):
        return '{expt}/{sample}'.format(
            bucket=cfg['S3_BUCKET'],
            expt = self.experiment['Name'],
            sample=self.sample_id)

    @property
    def experiment(self):
        if not hasattr(self, '_experiment'):
            expt_key = self.sample['Experiment'][0]
            self._experiment = client.get_record(expt_key, cfg['AIRTABLE_EXPT_TABLE'])['fields']
        return self._experiment
