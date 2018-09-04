import logging

from luigi import Parameter, WrapperTask

from ob_pipelines.entities.persistence import get_samples_by_experiment_id
from ob_pipelines.pipelines.rnaseq.tasks.kallisto import Kallisto
from ob_pipelines.pipelines.rnaseq.tasks.kallisto_spliced import KallistoSpliced
from ob_pipelines.pipelines.rnaseq.tasks.star import Star
from ob_pipelines.tasks.fastqc import FastQC
from ob_pipelines.tasks.gene_coverage import GeneCoverage
from ob_pipelines.tasks.index_bam import IndexBam
from ob_pipelines.tasks.merge_ercc import MergeERCC
from ob_pipelines.tasks.merge_kallisto import MergeKallisto
from ob_pipelines.tasks.read_distribution import ReadDistribution
from ob_pipelines.config import cfg
from ob_pipelines.tasks.s3sync import S3Sync
from ob_pipelines.tasks.scale_cluster import ScaleCluster, ScalingAction

logger = logging.getLogger('luigi-interface')


class RnaSeq(WrapperTask):
    expt_id = Parameter()

    def requires(self):
        yield ScaleCluster(desired_capacity_target=1, scaling_action=ScalingAction.UP)
        yield S3Sync(sync_id=self.expt_id, source=cfg['RAW_BUCKET'] + '/reference', destination='/reference', priority=90)
        for sample_id in get_samples_by_experiment_id(self.expt_id):
            yield FastQC(sample_id=sample_id)
            yield Star(sample_id=sample_id)
            yield IndexBam(sample_id=sample_id)
            yield Kallisto(sample_id=sample_id)
            yield GeneCoverage(sample_id=sample_id)
            yield ReadDistribution(sample_id=sample_id)
            yield KallistoSpliced(sample_id=sample_id)
        yield MergeKallisto(expt_id=self.expt_id)
        yield MergeERCC(expt_id=self.expt_id)
        yield ScaleCluster(desired_capacity_target=0, scaling_action=ScalingAction.DOWN)
