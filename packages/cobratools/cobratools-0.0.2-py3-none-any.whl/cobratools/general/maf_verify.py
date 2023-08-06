# -*- coding: utf-8 -*-
"""
Fetch nucleotides from genome data and compare sequence from MAF file
"""

import argparse
import os

from cobratools.general.models.maf import Maf


def run(infile):
    """
    Just do it
    :param infile: str
    """
    infile = os.path.join(os.getcwd(), infile)
    errors = Maf.maf_verify(infile)
    return errors


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", '--file',
                        type=str, required=True,
                        help="input MAF file")
    ARGS = parser.parse_args()

    MAF_FILEPATH = ARGS.file
    try:
        ERRORS = run(MAF_FILEPATH)
        print('{} mismatches encountered in {}'.format(ERRORS, MAF_FILEPATH))
    except FileNotFoundError:
        print("File {} not found".format(MAF_FILEPATH))
        exit(1)
    exit(0)
