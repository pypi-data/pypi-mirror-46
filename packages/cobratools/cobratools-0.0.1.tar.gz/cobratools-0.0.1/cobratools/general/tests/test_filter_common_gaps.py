# -*- coding: utf-8 -*-
"""
Tests for CommonGapFilter
"""

import pytest

# pylint: disable = E0401
# noinspection PyPackageRequirements
from Bio import AlignIO
# pylint: disable = E0401
# noinspection PyPackageRequirements
from Bio.Alphabet import single_letter_alphabet
# pylint: disable = E0401
# noinspection PyPackageRequirements
from Bio.Seq import Seq

from cobratools.general.models.filters import CommonGapFilter


def test_common_gap_filter():
    """
    General functional test. Are common gaps removed?
    """
    msa = None
    maf_file = './tests/data/test-1.maf'
    alignment_blocks = AlignIO.parse(maf_file, "maf")
    for msa in alignment_blocks:
        msa = CommonGapFilter.filter(msa)
    s_0 = Seq('TGGGG-------------------AAGCAGATTCAAACACAACTGTTTTAATTTGCAAAA'
              'TCATGGAATTAGCCTATGCTGCATAGGTGATGGTGTAGAATGTCATATGA-TTTT',
              single_letter_alphabet)
    s_1 = Seq('CTAGAACTGTTTTTAAATATGAAGAAATGGGTTCCAATATAATTGTAG-AGTTTACAGCA'
              'GTATGGAATTGACCCCTGCTTCATAGTTGATATTTTGGATTGCTTTATGATTTTT',
              single_letter_alphabet)
    s_2 = Seq('CCAGAACTGTTTTTAAATATGGGGAAATGGAGTCCAATATAACTGTAG-AGTTTATAGCA'
              'GCATAGAATTGACCTACGCTGCATAGTTGGTACTTTGGATTGCCTTATGA-TTTT',
              single_letter_alphabet)
    s_3 = Seq('CCAGAACTGTTTTTAAGTATGGGGAAATGGATTCTAATATAACTGTAG-AGTTTATAGCA'
              'GCATAGAATTGACCTGTGCTGCATAGTTGGTACTTTGGGTTGTCTTATGA-TTTT',
              single_letter_alphabet)
    s_4 = Seq('-------------------TGGGGTAATGGCTCTTAATGTAATGATAG-ACTTTACAACA'
              'GTGTGGAATTGACCTATGCTATATGGTTGATATTCTGGATTGCCTTTTGA-TTTT',
              single_letter_alphabet)
    assert msa[0].seq == s_0
    assert msa[1].seq == s_1
    assert msa[2].seq == s_2
    assert msa[3].seq == s_3
    assert msa[4].seq == s_4


@pytest.mark.skip
def test_increment_start_on_leading_common_gap():
    """
    There are 55 *leading* common gaps in each sequence in test file.
    Make sure start index for each sequence record has been incremented
    by the correct amount.
    """
    msa = None
    g = 55
    maf_file = './tests/data/test-2.maf'
    alignment_blocks = AlignIO.parse(maf_file, "maf")
    for msa in alignment_blocks:
        msa = CommonGapFilter.filter(msa)
    assert msa[0].annotations['start'] == 77462645 + g
    assert msa[1].annotations['start'] == 174613 + g
    assert msa[2].annotations['start'] == 24185 + g
    assert msa[3].annotations['start'] == 35766821 + g
    assert msa[4].annotations['start'] == 24782956 + g
    assert msa[5].annotations['start'] == 23954643 + g
    assert msa[6].annotations['start'] == 185783 + g
    assert msa[7].annotations['start'] == 72440405 + g
    assert msa[8].annotations['start'] == 3705014 + g
    assert msa[9].annotations['start'] == 263388 + g
    assert msa[10].annotations['start'] == 25141 + g
    assert msa[11].annotations['start'] == 111284 + g
    assert msa[12].annotations['start'] == 22679870 + g
    assert msa[13].annotations['start'] == 2122 + g
    assert msa[14].annotations['start'] == 24334982 + g
    assert msa[15].annotations['start'] == 1271292 + g
    assert msa[16].annotations['start'] == 1274 + g


def test_start_unchanged_if_no_leading_common_gap():
    """
    Make sure that if there are no leading common gaps, that start index for
    each sequence record remains unchanged
    """
    msa = None
    maf_file = './tests/data/test-1.maf'
    alignment_blocks = AlignIO.parse(maf_file, "maf")
    for msa in alignment_blocks:
        msa = CommonGapFilter.filter(msa)
    assert msa[0].annotations['start'] == 3950038
    assert msa[1].annotations['start'] == 91556186
    assert msa[2].annotations['start'] == 73773991
    assert msa[3].annotations['start'] == 80538394
    assert msa[4].annotations['start'] == 77462645


def test_nts_agreement():
    """
    Make sure nucleotide count matches what appears in annotations -- this
    should not change when removing common gaps. We need to be careful about
    how we go about this. We need to handle soft-masked regions (i.e., in
    lowercase), and may want to support extended alphabets. So best approach
    is to remove all gap symbols and count what's left.
    """
    msa = None
    maf_file = './tests/data/test-1.maf'
    alignment_blocks = AlignIO.parse(maf_file, "maf")
    for msa in alignment_blocks:
        msa = CommonGapFilter.filter(msa)
    assert msa[0].annotations['size'] == 95
    assert msa[1].annotations['size'] == 114
    assert msa[2].annotations['size'] == 113
    assert msa[3].annotations['size'] == 113
    assert msa[4].annotations['size'] == 94
    assert len(str(msa[0].seq).replace('-', '')) == 95
    assert len(str(msa[1].seq).replace('-', '')) == 114
    assert len(str(msa[2].seq).replace('-', '')) == 113
    assert len(str(msa[3].seq).replace('-', '')) == 113
    assert len(str(msa[4].seq).replace('-', '')) == 94
