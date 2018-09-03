from luigi import Parameter
from luigi.contrib.s3 import S3Target

from ob_pipelines import LoggingTaskWrapper
from ob_pipelines.apps.kallisto import merge_column
from ob_pipelines.config import cfg
from ob_pipelines.entities.persistence import get_samples_by_experiment_id
from ob_pipelines.s3 import csv_to_s3
from ob_pipelines.tasks.ercc_quant import ERCCQuant


class MergeERCC(LoggingTaskWrapper):
    expt_id = Parameter()

    def requires(self):
        return {
            sample_id: ERCCQuant(sample_id=sample_id)
            for sample_id in get_samples_by_experiment_id(self.expt_id)
        }

    def output(self):
        prefix = '{}/{}/'.format(cfg['S3_BUCKET'], self.expt_id)
        return {
            'est_counts': S3Target(prefix + 'ercc.unstranded.est_counts.csv'),
            'tpm': S3Target(prefix + 'ercc.unstranded.tpm.csv')
        }

    def run(self):
        # Gather input filepaths and labels
        tgt_dict = self.input()
        sample_ids = list(tgt_dict.keys())
        fpaths = [tgt_dict[sample_id]['abundance'].path for sample_id in sample_ids]

        # Merge columns
        annotations, est_counts = merge_column(fpaths, sample_ids, data_col='est_counts', annot=False)
        annotations, tpm = merge_column(fpaths, sample_ids, data_col='tpm', annot=False)

        csv_to_s3(est_counts, self.output()['est_counts'].path)
        csv_to_s3(tpm, self.output()['tpm'].path)
