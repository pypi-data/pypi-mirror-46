# -*- coding: utf-8 -*-
"""
Usage: python ./tools/kill_missing_ref.py /path/to/maf/file /path/to/out/dir ref_species

"""

import os
import sys
from pathlib import Path

# pylint: disable=E0401
from Bio import AlignIO
from general.models import MissingReferenceFilter


def process_maf(maf_filepath, out_filepath, ref_species):
    """
    :param maf_filepath: str
    :param out_filepath: str
    :param ref_species: str
    :return:
    """
    maf_filename = Path(maf_filepath).name
    outfile = os.path.join(out_filepath,
                           "refv_" +
                           maf_filename)
    with open(outfile, "w") as fh:
        writer = AlignIO.MafIO.MafWriter(fh)
        for msa in AlignIO.parse(maf_filepath, "maf"):
            msa = MissingReferenceFilter.filter(msa, ref_species)
            if msa is not None:
                writer.write_alignment(msa)


def run():
    """
    Run
    """
    maf = sys.argv[1]
    out = sys.argv[2]
    ref = sys.argv[3]

    os.makedirs(out, exist_ok=True)

    print(maf)

    process_maf(maf, out, ref)


if __name__ == '__main__':
    run()
