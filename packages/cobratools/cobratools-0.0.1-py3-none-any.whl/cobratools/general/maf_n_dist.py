# -*- coding: utf-8 -*-
"""
Count alignments by length
"""

import argparse
from typing import Dict, Tuple

# pylint: disable = E0401
# noinspection PyPackageRequirements
from Bio import AlignIO


def process_maf(filepath: str) -> Tuple[int, Dict[int, int]]:
    """
    Count alignments by length and return binned data
    :param filepath:
    :return:
    """
    num_blocks = 0
    bins = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0,
            6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    for blocks in AlignIO.parse(filepath, "maf"):
        num_blocks += 1
        bins[len(blocks)] += 1
    return num_blocks, bins


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", '--file',
                        type=str, required=True,
                        help="input MAF file")
    ARGS = parser.parse_args()

    MAF_FILEPATH = ARGS.file
    try:
        N_BLOCKS, BINS = process_maf(MAF_FILEPATH)
        print(BINS)
    except FileNotFoundError:
        print("File {} not found".format(MAF_FILEPATH))
        exit(1)
    exit(0)
