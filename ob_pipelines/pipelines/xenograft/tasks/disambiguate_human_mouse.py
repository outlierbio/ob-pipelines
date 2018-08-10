from luigi.contrib.s3 import S3Target

from ob_pipelines.batch import BatchTask, LoggingTaskWrapper
from ob_pipelines.config import cfg
from ob_pipelines.entities.sample import Sample
from ob_pipelines.pipelines.xenograft.tasks.star_by_species import StarBySpecies


class DisambiguateHumanMouse(BatchTask, LoggingTaskWrapper, Sample):
    job_definition = 'disambiguate'

    @property
    def parameters(self):
        outdir = '{}/{}/disambiguate/'.format(cfg['S3_BUCKET'], self.sample_folder)
        return {
            'outdir': outdir,
            'sample': self.sample_id,
            'aligner': 'star',
            'A': self.input()['human']['bam'].path,
            'B': self.input()['mouse']['bam'].path
        }

    def requires(self):
        return {
            'human': StarBySpecies(sample_id=self.sample_id, species='human'),
            'mouse': StarBySpecies(sample_id=self.sample_id, species='mouse')
        }

    def output(self):
        output_files = {
            'human': '{}{}.disambiguatedSpeciesA.bam',
            'mouse': '{}{}.disambiguatedSpeciesB.bam',
            'human_ambiguous': '{}{}.ambiguousSpeciesA.bam',
            'mouse_ambiguous': '{}{}.ambiguousSpeciesB.bam',
            'summary': '{}{}_summary.txt'
        }
        s3_paths = {k: v.format(self.parameters['outdir'], self.parameters['sample'])
                    for k, v in output_files.items()}
        return {k: S3Target(path) for k, path in s3_paths.items()}
