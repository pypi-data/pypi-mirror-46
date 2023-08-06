# -*- coding: utf-8 -*-
"""
Distill RNAz output to FASTA (without the fluff)

Also keeps track of chromosomes / segments we've encountered and writes list
to file.

Usage:

    python ./tools/rnaz_distill.py ./output/2019-03-17-b/rnaz_chr3.out

"""

import os
import sys

START = '>mm10'

OUT_DIR = '/users/c/b/cbcafier/rna_struct/output/temp/'
# OUT_DIR = '/Users/clayton/Workspace/RNA/RNA_Structure/output/temp/'

ALL_GENOME_FILE = '/users/c/b/cbcafier/scratch/data/genome/all.genome'
# ALL_GENOME_FILE = '/Users/clayton/Workspace/RNA/RNA_Structure/data/genome/all.genome'

HEADER_DELIMITER = '############################  RNAz 2.1  ##############################'
FASTA_DELIMITER = '######################################################################'


def parse_line(l):
    try:
        tokens = l.split(' ')
        chrom = tokens[0][1:]
        start = tokens[1]
        length = int(tokens[2])
        strand = tokens[3]
        max_len = int(tokens[4])
    except IndexError:
        print(l)
    return chrom, start, length, strand, max_len


def run(infile):
    """
    Just do it
    :param infile:
    """
    with open(infile, "r") as fh:
        records = 0
        lines = 0
        l_1 = True
        chroms = {}
        fa_1 = False  # Flag for first FASTA line, e.g. >SOMETHING
        fa_2 = False  # Flag for second FASTA line, e.g. AGCAGG....
        while l_1:
            l_1 = fh.readline()
            lines += 1
            if l_1.strip() == FASTA_DELIMITER:
                outfile_name = None
                within_fa = True
                sequences = 0
                records += 1
                while within_fa:
                    # We are within FASTA portion of RNAz output
                    l_2 = fh.readline()
                    lines += 1
                    if l_2.startswith(
                            ">consensus") or l_2.strip() == HEADER_DELIMITER:
                        # Bail out
                        break
                    if l_2.startswith(">"):
                        fa_1 = True
                        fa_2 = False
                        if sequences == 0:
                            # This should be the first
                            if not l_2.startswith(START):
                                # mm10 is not first sequence!
                                print("Ref species not first in FASTA")
                                print(l_2)
                                within_fa = False
                                outfile_name = None
                            else:
                                # This is our mm10 reference sequence
                                sequences = 1
                                chrom, start, length, strand, max_len = \
                                    parse_line(l_2)
                                if strand == '+':
                                    direction = 'fwd'
                                elif strand == '-':
                                    direction = 'rev'
                                else:
                                    direction = 'unk'
                                outfile_name = chrom + '_' + start + \
                                               '_' + direction + '.fa'
                                if chrom not in chroms.keys():
                                    chroms[chrom] = max_len
                                try:
                                    os.remove(
                                        os.path.join(OUT_DIR, outfile_name))
                                except OSError:
                                    pass
                        else:
                            # sequences != 0
                            sequences += 1
                            if l_2.startswith(">"):
                                chrom, start, length, strand, max_len = \
                                    parse_line(l_2)
                                if chrom not in chroms.keys():
                                    chroms[chrom] = max_len
                    if outfile_name is not None:
                        p = os.path.join(OUT_DIR, outfile_name)
                        with open(p, 'a') as outfile:
                            if fa_1:
                                outfile.write(l_2)
                                fa_1 = False
                                fa_2 = True
                            elif fa_2:
                                outfile.write(
                                    l_2.replace("-", ""))  # remove gaps
                                fa_2 = False
                            else:
                                fa_1 = False
                                fa_2 = False
    print("{} lines read".format(lines))
    print("{} records encountered".format(records))
    line = True
    d = {}
    with open(ALL_GENOME_FILE, "r") as fh:
        while line:
            line = fh.readline()
            if not line.startswith("#") and line.strip():
                tokens = line.split('\t')
                d[tokens[0]] = tokens[1].strip()
    with open(ALL_GENOME_FILE, "a") as fh:
        for key, value in chroms.items():
            if key not in d.keys():
                fh.write("{}\t{}\n".format(key, value))
    print("Done")


if __name__ == '__main__':

    INFILE = sys.argv[1]
    print("INFILE = {}".format(INFILE))
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    run(INFILE)
