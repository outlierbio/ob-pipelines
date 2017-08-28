from ob_pipelines import s3
import pysam
import sys

@s3.s3args()
def dedupe_by_pos_strand(infile, outfile):

    infile = pysam.AlignmentFile(infile, 'rb')
    outfile = pysam.AlignmentFile(outfile, 'wb', template=infile)
    
    pos_list = set()
    for aln in infile:
        pos_strand = (aln.reference_start, aln.is_reverse)
        if aln.reference_start == -1:
            continue
        if pos_strand in pos_list:
            continue
        outfile.write(aln)
        pos_list.add(pos_strand)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: {} INFILE OUTFILE'.format(sys.argv[0]))
        sys.exit(0)

    _, infile, outfile = sys.argv
    dedupe_by_pos_strand(infile, outfile)