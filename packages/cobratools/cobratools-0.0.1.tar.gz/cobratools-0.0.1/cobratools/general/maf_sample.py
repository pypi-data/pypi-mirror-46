# -*- coding: utf-8 -*-
"""
Sample sequences from MAF file(s) with suitable coverage by specified species
We randomly sample i.i.d. with prob = p

Usage: python ./tools/maf_sample.py /path/to/maf/file [p]
"""

import argparse
import random
import sys
from typing import Tuple

# pylint: disable = E0401
# noinspection PyPackageRequirements
from Bio import AlignIO

from cobratools.general.config import CONF


def process_maf(maf_filepath: str, p: float) -> Tuple[int, int]:
    """
    Sample source data with specified coverage with probability p

    :param maf_filepath: str
    :param p: float
    :return: int, int
    """
    num_blocks = 0
    num_selected = 0
    writer = AlignIO.MafIO.MafWriter(sys.stdout)  # we're writing to stdout
    for block in AlignIO.parse(maf_filepath, "maf"):
        num_blocks += 1
        if random.random() <= p:
            num_selected += 1
            writer.write_alignment(block)
    return num_blocks, num_selected


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", '--file',
                        type=str, required=True,
                        help="input MAF file")
    parser.add_argument("-p", '--probability',
                        type=int, default=CONF['SAMPLE_PROB'],
                        help="probability")
    ARGS = parser.parse_args()

    MAF_FILEPATH = ARGS.file
    SAMPLE_PROB = ARGS.probability
    try:
        assert 0 < SAMPLE_PROB <= 1.0
    except AssertionError:
        print("Invalid probability. Must be in interval (0, 1.0]")
        exit(1)
    N_BLOCKS, N_SELECTED = process_maf(MAF_FILEPATH, SAMPLE_PROB)
    PCT = float(N_SELECTED) / float(N_BLOCKS)
    print('{} blocks; {} selected; {:.2%}'.format(N_BLOCKS, N_SELECTED, PCT))
    exit(0)
