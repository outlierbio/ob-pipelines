from datetime import datetime

from luigi import Parameter

from ob_pipelines.config import cfg


class Sample(object):
    sample_id = Parameter()

    def __init__(self, *args, **kwargs):

        if 'id' in kwargs:
            self.key = kwargs['id']

        if 'fields' in kwargs:
            self._sample = kwargs['fields']

        if 'createdTime' in kwargs:
            self._created_at = kwargs['createdTime']
        else:
            self._created_at = datetime.utcnow()


    @property
    def sample(self):
        # TODO: remove fallback init
        if not hasattr(self, '_sample'):
            from ob_pipelines.entities.persistence import get_sample_by_name
            self._sample = get_sample_by_name(self.sample_id)
        return self._sample

    @property
    def sample_folder(self) -> str:
        return '{expt}/{sample}'.format(
            bucket=cfg['S3_BUCKET'],
            expt=self.experiment.name,
            sample=self.sample_id)

    @property
    def experiment(self):
        # TODO: remove fallback init
        if not hasattr(self, '_experiment'):
            expt_key = self.sample.sample['Experiment'][0]
            from ob_pipelines.entities.persistence import get_experiment_by_key
            self._experiment = get_experiment_by_key(expt_key)
        return self._experiment

    @experiment.setter
    def experiment(self, value):
        self._experiment = value
