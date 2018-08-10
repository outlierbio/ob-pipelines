from ob_pipelines.config import cfg
from ob_pipelines.pipelines.rnaseq.tasks.star import Star
from ob_pipelines.tasks.skewer import Skewer


class StarBySpecies(Star):

    def requires(self):
        return Skewer(sample_id=self.sample_id)

    def prefix(self):
        return '{}/{}/star/{}.{}.'.format(
            cfg['S3_BUCKET'], self.sample_folder, self.sample_id, self.species)
