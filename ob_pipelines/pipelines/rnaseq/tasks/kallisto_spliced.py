from luigi.contrib.s3 import S3Target

from ob_pipelines.config import cfg
from ob_pipelines.pipelines.rnaseq.tasks.bam_to_fastq import BamToFastQ
from ob_pipelines.pipelines.rnaseq.tasks.kallisto import Kallisto


class KallistoSpliced(Kallisto):

    def requires(self):
        return BamToFastQ(sample_id=self.sample_id)

    def output(self):
        output_files = {
            'abundance': 'abundance.tsv',
            'h5': 'abundance.h5',
            'run_info': 'run_info.json'
        }
        return {k: S3Target('{}/{}/filtered/{}'.format(cfg['S3_BUCKET'], self.sample_folder, fname))
                for k, fname in output_files.items()}
