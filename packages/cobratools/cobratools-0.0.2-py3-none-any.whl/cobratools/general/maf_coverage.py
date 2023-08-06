# -*- coding: utf-8 -*-
"""
Scan MAF file(s) to check for coverage by specified species
"""

import argparse
from typing import List, Tuple, Dict

# pylint: disable = E0401
# noinspection PyPackageRequirements
from Bio import AlignIO


def get_targets(s: str) -> List[str]:
    """
    Input is comma-separated list of species, e.g., mm10,oryCun2,panTro4
    Output is list, e.g. ['mm10', 'oryCun2', 'panTro4']
    :param s: str
    :return: list
    """
    if s is None:
        return []
    return s.split(',')


def process_maf(filepath: str, targets: List[str]) -> Tuple[int, int]:
    """
    Check coverage of specified MAF file

    :param filepath:
    :param targets:
    :return:
    """
    num_blocks = 0
    num_ok = 0
    match_srs: Dict = {}
    num_species = len(targets)
    for block in AlignIO.parse(filepath, "maf"):
        num_blocks += 1
        n = 0
        for sr in block:
            species = sr.id.split('.')[0]
            if species in targets:
                if sr.id not in match_srs.keys():
                    match_srs[sr.id] = 1
                else:
                    match_srs[sr.id] += 1
                n += 1
        if n == num_species:
            num_ok += 1
    return num_blocks, num_ok


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", '--file',
                        type=str, required=True,
                        help="input MAF file")
    parser.add_argument("-s", '--target-species',
                        type=str,
                        help="target species (comma separated list)")
    ARGS = parser.parse_args()
    TARGETS = get_targets(ARGS.target_species)
    MAF_FILEPATH = ARGS.file
    try:
        N_BLOCKS, N_OK = process_maf(MAF_FILEPATH, TARGETS)
        PCT = N_OK / N_BLOCKS
        print('{} blocks; {} covered; {:.2%}'.format(N_BLOCKS,
                                                     N_OK,
                                                     PCT))
    except FileNotFoundError:
        print("File {} not found".format(MAF_FILEPATH))
        exit(1)
    exit(0)
