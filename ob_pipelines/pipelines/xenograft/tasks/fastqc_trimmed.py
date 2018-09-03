from ob_pipelines.tasks.fastqc import FastQC
from ob_pipelines.tasks.skewer import Skewer


class FastQCTrimmed(FastQC):

    def requires(self):
        return Skewer(sample_id=self.sample_id)
