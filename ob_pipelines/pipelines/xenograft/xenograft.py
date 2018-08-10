from luigi import Parameter, WrapperTask

from ob_pipelines.entities.persistence import get_samples_by_experiment_id
from ob_pipelines.pipelines.xenograft.tasks.bam_to_fastq import BamToFastQ
from ob_pipelines.pipelines.xenograft.tasks.fastqc_trimmed import FastQCTrimmed


class Run(WrapperTask):

    expt_id = Parameter()

    def requires(self):
        for sample_id in get_samples_by_experiment_id(self.expt_id):
            yield FastQCTrimmed(sample_id=sample_id)
            yield BamToFastQ(sample_id=sample_id)
