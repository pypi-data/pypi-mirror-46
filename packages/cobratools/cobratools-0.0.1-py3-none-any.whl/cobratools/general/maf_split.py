# -*- coding: utf-8 -*-
"""
Split MAF by chromosome

We assume a few things. First, we assume that MAF file is sorted.

Second, we assume that first species in the multiple sequence alignment is
the reference and we should use this species.chromosome to split file.

We don't implement this as a filter (returning results to stdout) as we wish
to write to multiple files automatically.
"""

import argparse
from typing import Generator, Tuple

# pylint: disable = E0401
# noinspection PyPackageRequirements
from Bio import AlignIO, SeqRecord
# pylint: disable = E0401
# noinspection PyPackageRequirements
from Bio.Align import MultipleSeqAlignment


def get_chrom(sr: SeqRecord) -> str:
    """
    :param sr: SeqRecord
    :return: str
    """
    return sr.id.split('.')[1]


def write_chrom(chrom: str, block: MultipleSeqAlignment, blocks: Generator) \
        -> Tuple[str, MultipleSeqAlignment, Generator]:
    """
    Write all blocks for this chromosome. Assumes MAF file is sorted.
    :param block: MultipleSeqAlignment
    :param blocks: generator
    :param chrom: str
    :return:
    """
    with open(chrom + '.maf', "w") as fh:
        writer = AlignIO.MafIO.MafWriter(fh)
        this_chrom = chrom
        while this_chrom == chrom:
            writer.write_alignment(block)
            try:
                block = next(blocks)
                chrom = get_chrom(block[0])
            except StopIteration:
                chrom = ''  # empty string
    return chrom, block, blocks


def split(maf: str):
    """
    :param maf: Filename
    :return:
    """
    blocks = AlignIO.parse(maf, 'maf')  # Returns a generator
    block = next(blocks)
    chrom = get_chrom(block[0])
    while chrom:
        chrom, block, blocks = write_chrom(chrom, block, blocks)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", '--file',
                        type=str, required=True,
                        help="input MAF file")

    ARGS = parser.parse_args()

    MAF_FILEPATH = ARGS.file
    try:
        split(MAF_FILEPATH)
    except FileNotFoundError:
        print("File {} not found".format(MAF_FILEPATH))
        exit(1)
    exit(0)
