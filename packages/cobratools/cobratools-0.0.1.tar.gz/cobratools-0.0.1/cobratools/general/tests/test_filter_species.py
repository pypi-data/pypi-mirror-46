# -*- coding: utf-8 -*-
"""
Tests for SpeciesFilter
"""

# pylint: disable=E0401
# noinspection PyPackageRequirements
from Bio import AlignIO

# pylint: disable=W0611
from cobratools.general.models.filters import SpeciesFilter


def test_filter_species():
    """
    Test filter species
    INCOMPLETE
    """
    maf_file = './tests/data/test-2.maf'
    alignment_blocks = AlignIO.parse(maf_file, "maf")
    species_list = ['mm10', 'susScr3', 'oryCun2', 'panTro4', 'rheMac3']
    for msa in alignment_blocks:
        # noinspection PyUnusedLocal
        msa = SpeciesFilter.filter(msa, species_list)
