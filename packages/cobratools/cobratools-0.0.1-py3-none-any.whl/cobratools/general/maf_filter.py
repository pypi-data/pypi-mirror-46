# -*- coding: utf-8 -*-
"""
Sample sequences from MAF file(s) with suitable coverage by specified species
We randomly sample with prob p i.i.d.

Filter MAF data on selected species. Note that common gaps are removed
from selected alignments.

Usage: python ./tools/maf_sample.py /path/to/maf/file

e.g.  python ./py/maf_sample.py ~/scratch/data/multiz/chr19.maf

"""

import argparse
import sys
from typing import Dict, Tuple, List

# pylint: disable = E0401
# noinspection PyPackageRequirements
from Bio import AlignIO

from cobratools.general.models.filters import SpeciesFilter, CommonGapFilter, \
    GenomeCheckFilter


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


def process_maf(maf_filepath: str, opts: Dict) -> Tuple[int, int]:
    """
    Sample source data with specified coverage with probability SAMPLE_PROB

    Actually, the pct is % of alignments rejected because of failed genome
    check. Many will be rejected before getting to this test (e.g., too short,
    insufficient coverage, not sampled).

    :param maf_filepath: str
    :param opts: dict
    :return: int, int
    """
    num_blocks = 0
    num_filtered = 0
    writer = AlignIO.MafIO.MafWriter(sys.stdout)  # we're writing to stdout
    for block in AlignIO.parse(maf_filepath, "maf"):
        num_blocks += 1
        ok = True
        if opts['size']:
            # Only pick alignments of >= min size
            if block[0].annotations['size'] < opts['size']:
                ok = False
        if ok and opts['targets']:
            # Make sure all target species are present
            species = []
            for sr in block:
                species.append(sr.id.split('.')[0])
            i = list(set(species) & set(opts['targets']))
            if len(i) != len(opts['targets']):
                ok = False
            if ok and opts['restrict']:
                # Remove any species not among target species
                block = SpeciesFilter.filter(block, opts['targets'])
                block = CommonGapFilter.filter(block)
        if ok and opts['verify']:
            # Verify data against genome
            block = GenomeCheckFilter.filter(block)
            if block is None:
                ok = False
        if ok:
            # We've made it
            num_filtered += 1
            writer.write_alignment(block)
    return num_blocks, num_filtered


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", '--file',
                        type=str, required=True,
                        help="input MAF file")
    parser.add_argument("-l", '--min-length',
                        type=int, default=0,
                        help="min length for alignment (residues)")
    parser.add_argument("-s", '--target-species',
                        type=str,
                        help="target species (comma separated list)")
    # --restrict option only relevant if target species list given
    parser.add_argument("--restrict",
                        action="store_true",
                        help="restrict alignments to target species only")
    parser.add_argument("--verify",
                        action="store_true",
                        help="verify alignments against genome data")
    ARGS = parser.parse_args()
    MAF_FILEPATH = ARGS.file
    OPTS = {'size': ARGS.min_length,
            'targets': get_targets(ARGS.target_species),
            'restrict': ARGS.restrict,
            'verify': ARGS.verify}
    try:
        N_BLOCKS, N_FILTERED = process_maf(MAF_FILEPATH, OPTS)
        PCT = float(N_FILTERED) / float(N_BLOCKS)
        print('{} blocks; {} filtered; {:.2%}'.format(N_BLOCKS,
                                                      N_FILTERED,
                                                      PCT))
    except FileNotFoundError:
        print("File {} not found".format(MAF_FILEPATH))
        exit(1)
    exit(0)
