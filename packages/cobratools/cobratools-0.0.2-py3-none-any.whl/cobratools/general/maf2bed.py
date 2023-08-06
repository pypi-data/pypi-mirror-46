# -*- coding: utf-8 -*-
"""
Convert MAF to BED
"""

import argparse

# pylint: disable = E0401
# noinspection PyPackageRequirements
from Bio import AlignIO

from cobratools.general.models.bed import BedLine


def run(fn, ref):
    """
    Just do it

    BED file requires chrom, chromStart, chromEnd
    Optional: name, score, strand, thickStart, thickEnd, itemRgb,
              blockCount, blockSizes, blockStarts

    See: https://genome.ucsc.edu/FAQ/FAQformat.html#format1

    Thiel's BED file specimen:

    chrom   chromStart  chromEnd    name        score  str  ...
    chr10	18268594	18268759	loc457756	200	   -	...
    From here on, it seems they've taken liberties....
    -57.60	   0.994181	mm10.rn5	0.55054	0.78	rRNA
    """
    maf = AlignIO.parse(fn, "maf")
    for msa in maf:
        for sr in msa:
            if sr.id.startswith(ref):
                bed_line = BedLine({'chrom': sr.id.split('.')[1],
                                    'chromStart': sr.annotations['start'],
                                    'chromEnd': int(sr.annotations['start'])
                                                + int(sr.annotations['size']),
                                    'name': sr.id,
                                    'score': 0,
                                    'strand': sr.annotations['strand'],
                                    'thickStart': None,
                                    'thickEnd': None,
                                    'itemRgb': None,
                                    'blockCount': None,
                                    'blockSizes': None,
                                    'blockStarts': None})
                print(bed_line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", '--file',
                        type=str, required=True,
                        help="input MAF file")
    parser.add_argument("-r", '--reference-species',
                        type=str,
                        help="reference species, e.g., mm10, hg19")
    ARGS = parser.parse_args()
    MAF_FILEPATH = ARGS.file
    REFERENCE_SPECIES = ARGS.reference_species
    try:
        run(MAF_FILEPATH, REFERENCE_SPECIES)
    except FileNotFoundError:
        print("File {} not found".format(MAF_FILEPATH))
        exit(1)
    exit(0)
