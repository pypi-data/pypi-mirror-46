# -*- coding: utf-8 -*-
"""
LocARNA output will be in directories with ".out" extension, e.g.

    mm10.chr3_3748045.flanked.out

Output alignment will be in results/result.aln within the above directory.

LocARNA does not include any metadata in the file other than the label for each
sequence in the alignment, e.g., oryCun2.chr3

Other data should be recovered from filename, etc. to construct MAF file for
input to RNAz
"""

import glob
import os

# pylint: disable = E0401
from Bio import AlignIO

TEMPLATE = """#PBS -l nodes=1:ppn=1
#PBS -l walltime=30:00:00
#PBS -N $NAME
#PBS -M cbcafier@uvm.edu
# Send email only on ABORT
#PBS -m a

cd $HOME/rna_struct/output
echo "This is $NAME running on " `hostname`
# Important that we use --locarnate switch in second screen
RNAz --locarnate --both-strands --cutoff=0.9 ./05_preprocessing/$NAME.maf > ./06_rnaz_2/$NAME.out
"""

LOCARNA_OUT_DIRS = ['./04_locarna']
REMAF_OUT_DIR = './05_preprocessing'
SCRIPT_OUT_DIR = './06_rnaz_2/scripts'


def run():
    """
    Just do it
    """
    msa = None
    d = {}
    for locarna_out_dir in LOCARNA_OUT_DIRS:
        locarna_out_list = glob.glob(os.path.join(locarna_out_dir, '*.out'))

        for locarna_out in locarna_out_list:
            locarna_aln_file = os.path.join(locarna_out, 'results',
                                            'result.aln')
            source_fa_file = os.path.splitext(locarna_out)[0] + '.fa'
            try:
                d = {}
                with open(source_fa_file, 'r') as fh:
                    # Can't use AlignIO.parse since sequences may be of
                    # different lengths (this file is input to LocARNA,
                    # not a proper MSA)
                    line = True
                    while line:
                        line = fh.readline()
                        if line.startswith(">"):
                            # >mm10.chr3 3748025 153 - 160039680 flanked, b=20
                            tokens = line[1:].split()
                            d[tokens[0]] = {
                                'start': tokens[1],
                                'size': tokens[2],
                                'strand': tokens[3],
                                'size_src': tokens[4]
                            }
                msas = AlignIO.parse(locarna_aln_file, "clustal")
                id_ = None
                start = None
                for msa in msas:
                    for sr in msa:
                        sr.annotations = d[sr.id]
                        if sr.id.startswith('mm10'):
                            id_ = sr.id
                            start = d[sr.id]['start']
                if id_ is not None and start is not None:
                    fn = id_ + "." + start
                    output_maf_file = os.path.join(REMAF_OUT_DIR, fn + ".maf")
                    output_script_file = \
                        os.path.join(SCRIPT_OUT_DIR, fn + ".script")
                    with open(output_maf_file, "w") as fh:
                        writer = AlignIO.MafIO.MafWriter(fh)
                        writer.write_alignment(msa)
                    with open(output_script_file, "w") as fh:
                        s = TEMPLATE
                        s = s.replace("$NAME", fn)
                        fh.write(s)
                else:
                    print("BAD ALN FILE: {}".format(locarna_aln_file))
            except FileNotFoundError as err:
                print(str(err))
            except Exception:
                print(d)
                raise


if __name__ == '__main__':
    run()
