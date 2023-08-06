# -*- coding: utf-8 -*-
"""
Merge overlapping windows

Unfortunately we can't use Bedtools merge at present
https://bedtools.readthedocs.io/en/latest/content/tools/merge.html
"""

import os
import sys

# pylint: disable=E0401
from Bio import AlignIO
# pylint: disable=E0401
from Bio import SeqIO

from rlr.models.merger import Merge


def process_locus(locus):
    """
    Given a locus consisting of overlapping alignment windows, merge individual
    sequences to form new merged locus.

    Locus might look something like this:

    locus2	mm10.chr3	3760617	3760772	2	98.33	0.992183	-2.84
    window2	locus2	mm10.chr3	3760617	3760737	+	2	120	98.33	-25.70	...
    window3	locus2	mm10.chr3	3760617	3760737	-	2	120	98.33	-33.15	...
    window4	locus2	mm10.chr3	3760637	3760757	+	2	120	97.50	-33.10	...
    window5	locus2	mm10.chr3	3760652	3760772	+	2	120	95.83	-32.70	...
    window6	locus2	mm10.chr3	3760652	3760772	-	2	120	95.83	-29.25	...

    or

    locus20	mm10.chr3	4605486	4605670	4	81.25	0.990061	-2.99
    window32	locus20	mm10.chr3	4605486	4605606	+	4	120	80.31	...
    window33	locus20	mm10.chr3	4605506	4605626	+	4	120	81.25	...
    window34	locus20	mm10.chr3	4605526	4605646	+	4	120	81.25	...
    window35	locus20	mm10.chr3	4605546	4605665	+	4	120	79.97	...
    window36	locus20	mm10.chr3	4605551	4605670	+	4	120	78.84	...

    Not sure what to do with the first case (mixed strands). The second case
    (all + strands) is more straightforward.

    :param locus:
    :return:
    """
    sequences = {}
    alignment_blocks = []
    strands = []
    for window in locus['windows']:
        strands.append(window['strand'])
    if len(list(set(strands))) != 1:
        # Heterogeneous directions. Not implemented yet.
        return False, False
    for window in locus['windows']:
        fn = os.path.join(RNAZ_DIR,
                          'results_' + locus['chr'],
                          locus['name'],
                          window['name'] + '.maf')
        alignment_blocks.append(AlignIO.parse(fn, "maf"))
    for msas in alignment_blocks:
        for msa in msas:
            # If reading a window file, there should be only one MSA. But
            # there will be two or more sequences per MSA
            for sr in msa:
                if sr.id in sequences.keys():
                    sequences[sr.id].append(sr)
                else:
                    sequences[sr.id] = [sr]
    for id_, seq_list in sequences.items():
        merged = seq_list[0]
        for another in seq_list[1:]:
            merged = Merge.merge_seq(merged, another)
        sequences[id_] = [merged]
    return sequences, locus


def write_fa(sequences, locus):
    """
    :param sequences
    :param locus
    :return:
    """
    fn = os.path.join(OUTDIR, locus['chr'] + '_' + locus['name'] + '.fa')
    print(fn)
    with open(fn, "w") as fh:
        for id_, lst in sequences.items():
            try:
                sr = lst[0]
                sr.annotations['size'] = sr.annotations['nts_merged']
                # print(id_, sr)
                SeqIO.write(sr, fh, "fasta")
            except Exception:
                print("Exception on locus {}".format(locus['name']))


def run():
    """
    Just do it
    """
    with open(INFILE, "r") as fh:
        line = True
        locus = {}
        while line:
            line = fh.readline()
            if line.startswith("locus"):
                if locus:
                    records, locus = process_locus(locus)
                    if records:
                        write_fa(records, locus)
                tokens = line.split()
                locus = {
                    'name': tokens[0],
                    'num': tokens[0][5:],  # strip off "locus"
                    'id': tokens[1],
                    'chr': tokens[1].split('.')[1],
                    'start': tokens[2],
                    'end': tokens[3],
                    'windows': []}
            elif line.startswith("window"):
                tokens = line.split()
                window = {
                    'name': tokens[0],
                    'num': tokens[0][7:],  # strip off "locus"
                    'locus': tokens[1],
                    'id': tokens[2],
                    'start': tokens[3],
                    'end': tokens[4],
                    'strand': tokens[5]}
                assert window['id'] == locus['id']
                assert window['locus'] == locus['name']
                locus['windows'].append(window)
            else:
                pass
                # ignore comments
    records, locus = process_locus(locus)  # The last one
    if records:
        write_fa(records, locus)


if __name__ == '__main__':

    try:
        INFILE = sys.argv[1]
        OUTDIR = sys.argv[2]
        RNAZ_DIR = sys.argv[3]
    except IndexError:
        print("Usage: python merge.py INPUT_FILE OUTPUT_DIR RNAZ_DIR")
        exit(1)
    run()
    exit(0)
