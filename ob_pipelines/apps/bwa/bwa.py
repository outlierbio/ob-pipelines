"""BWA wrapper scripts"""
import os
import os.path as op
from subprocess import check_output

SCRATCH_DIR = os.environ['SCRATCH_DIR']

import click
from ob_pipelines import s3


@s3.s3args()
def samse_s3_enabled(threads, reference, fq, bam):
    """Run aln followed by samse and sam > bam"""
    tmp_prefix = op.join(SCRATCH_DIR, op.basename(fq))
    cmd = """
        bwa aln -t {threads} {ref} {fq} > {tmp}.sai && \
        bwa samse {ref} {tmp}.sai {fq} > {tmp}.sam && \
        samtools view -@ {threads} -bh {tmp}.sam > {tmp}.bam && \
        samtools sort -@ {threads} -o {bam} {tmp}.bam
    """.format(
        ref = reference,
        fq = fq,
        tmp = tmp_prefix, 
        threads = threads,
        bam = bam
    )
    print(check_output(cmd, shell=True))


@click.command()
@click.argument('threads')
@click.argument('reference')
@click.argument('fq')
@click.argument('bam')
def samse(threads, reference, fq, bam):

    # BWA reference is a prefix, but s3args only downloads the specified file
    # Have to get the rest here.
    if reference.startswith('s3://'):
        print(check_output(['aws', 's3', 'cp', reference, SCRATCH_DIR]))

        for ext in ['.ann', '.amb', '.pac', '.sa', '.bwt']:
            print(check_output(['aws', 's3', 'cp', reference + ext, SCRATCH_DIR]))
        local_ref = op.join(SCRATCH_DIR, op.basename(reference))
    else:
        local_ref = reference

    samse_s3_enabled(threads, local_ref, fq, bam)


if __name__ == '__main__':
    samse()