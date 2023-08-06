# -*- coding: utf-8 -*-
"""
Count nts in MAF file or RNAz output file

Invoke thus: python ./tools/count_nts.py ./path/to/input_file.[maf|out]

"""

import os
import sys

# pylint: disable = E0401
from Bio import AlignIO


def process_maf(filepath):
    """
    Process file in MAF format

    :param filepath:
    :return:
    """
    nts = 0
    for ma in AlignIO.parse(filepath, "maf"):
        # ma is of type <class 'Bio.Align.MultipleSeqAlignment'>
        for sr in ma:
            # sr is of type <class 'Bio.SeqRecord.SeqRecord'>
            nts += sr.annotations['size']
    return nts


def process_rnaz_out(filepath):
    """
    Process file in RNAz output format

    :param filepath:
    :return:
    """
    nts = 0
    sequences = -1
    with open(filepath, "r") as fh:
        for line in fh:
            if line.startswith(' Sequences: '):
                x = line.split()
                sequences = int(x[1])
            if line.startswith(' Columns: '):
                x = line.split()
                columns = int(x[1])
                nts += sequences * columns
    return nts


def run():
    """
    Run
    """
    filepath = sys.argv[1]
    _, file_extension = os.path.splitext(filepath)
    if file_extension == '.maf':
        nts_ = process_maf(filepath)
    elif file_extension == '.out':
        nts_ = process_rnaz_out(filepath)
    else:
        raise Exception("Unsupported file type")
    print(nts_)


if __name__ == '__main__':
    run()
