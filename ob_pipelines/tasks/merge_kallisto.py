from luigi import Parameter, BoolParameter
from luigi.contrib.s3 import S3Target

from ob_pipelines import LoggingTaskWrapper
from ob_pipelines.apps.kallisto import merge_column
from ob_pipelines.config import cfg
from ob_pipelines.entities.persistence import get_samples_by_experiment_id
from ob_pipelines.pipelines.rnaseq.tasks.kallisto import Kallisto
from ob_pipelines.s3 import csv_to_s3


class MergeKallisto(LoggingTaskWrapper):
    expt_id = Parameter()
    annot = BoolParameter(False)

    def requires(self):
        return {
            sample_id: Kallisto(sample_id=sample_id)
            for sample_id in get_samples_by_experiment_id(self.expt_id)
        }

    def output(self):
        prefix = '{}/{}/'.format(cfg['S3_BUCKET'], self.expt_id)
        out_dict = {
            'est_counts': S3Target(prefix + 'est_counts.csv'),
            'tpm': S3Target(prefix + 'tpm.csv')
        }
        if self.annot:
            out_dict['annotations'] = S3Target(prefix + 'annotations.csv')
        return out_dict

    def run(self):
        # Gather input filepaths and labels
        tgt_dict = self.input()
        sample_ids = list(tgt_dict.keys())
        fpaths = [tgt_dict[sample_id]['abundance'].path for sample_id in sample_ids]

        # Merge columns
        annotations, est_counts = merge_column(fpaths, sample_ids, data_col='est_counts', annot=self.annot)
        annotations, tpm = merge_column(fpaths, sample_ids, data_col='tpm', annot=self.annot)

        if self.annot:
            csv_to_s3(annotations, self.output()['annotations'].path)
        csv_to_s3(est_counts, self.output()['est_counts'].path)
        csv_to_s3(tpm, self.output()['tpm'].path)
