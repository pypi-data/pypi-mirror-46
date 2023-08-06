# -*- coding: utf-8 -*-
"""
Models used by tools
"""

from typing import Optional

# pylint: disable = E0401
# noinspection PyPackageRequirements
from Bio.Align import MultipleSeqAlignment

from cobratools.general.models.btools import Bedtools
from cobratools.general.models.constants import GAP_SYMBOL


# pylint: disable=R0903
class GenomeCheckFilter:
    """
    Remove any sequences for which we don't have a match with genome data.
    Rationale: We have 60-species Multiz alignment from PSU as source, but we
    need to include flanking regions after first RNAz cut, before processing
    with LocARNA-P. However, when we have compared Multiz alignment data with
    chromosome data feched from UCSC, we find some mismatches. Ideally we'd
    like to drill down to determine the reason for each mismatch. Revision
    numbers and IDs for data seem to match but maybe there were patches applied
    or other changes. Some of these differences are really odd, e.g., Multiz
    MAF might contain ACGTTAAC for some species.chromosome position, but
    chromosome data from UCSC might have something entirely different --
    CACCCACC or NNNNNNNN, etc. We've confirmed this result using UCSC Genome
    Browser. How to resolve? Right now, we don't we toss the sequence. Then
    toss the alignment if we have thrown out more than one sequence. That is
    4/5 gets a pass.

    TODO: If reference species can't be verified, toss the whole alignment
    """

    @staticmethod
    def filter(msa: MultipleSeqAlignment, tolerance: int = 1) \
            -> Optional[MultipleSeqAlignment]:
        """
        Apply filter to MSA
        TODO implement use of softmask_ok
        :param msa:
        :param tolerance:
        :return:
        """
        passing_srs = []
        num_bad = 0
        reference = msa[0].id
        for sr in msa:
            ok, _ = Bedtools.verify_fasta(sr, reference, softmask_ok=True)
            if ok:
                passing_srs.append(sr)
            else:
                num_bad += 1
                if num_bad == tolerance + 1:
                    return None
        return MultipleSeqAlignment(passing_srs,
                                    annotations=msa.annotations)


# pylint: disable=R0903
class MissingReferenceFilter:
    """
    a score=0.00
    s mm10.chr16   << SHOULD BE IN MSA AND BE FIRST IN LINE
    """

    @staticmethod
    def filter(msa: MultipleSeqAlignment, ref_species: str) \
            -> Optional[MultipleSeqAlignment]:
        """
        Remove sequences with missing reference. If reference species is in
        alignment return alignment, otherwise return None

        :param msa:
        :param ref_species:
        :return:
        """
        for sr in msa:
            if sr.name.split('.')[0] == ref_species:
                return msa
        return None


# pylint: disable=R0903
class SpeciesFilter:
    """
    Remove non-target species from MSA

    Mode can be all (all listed species must be present) or any
    """

    @staticmethod
    def filter(msa: MultipleSeqAlignment,
               species_list: list,
               mode: str = 'all') -> Optional[MultipleSeqAlignment]:
        """
        Apply filter to exclude species not in list

        :param msa:
        :param species_list:
        :param mode: str
        :return:
        """
        target_srs = []
        for sr in msa:  # sr is of type <class 'Bio.SeqRecord.SeqRecord'>
            if sr.name.split('.')[0] in species_list:
                target_srs.append(sr)
        if target_srs:
            if mode == 'all':
                if len(target_srs) != len(species_list):
                    return None
            return MultipleSeqAlignment(target_srs,
                                        annotations=msa.annotations)
        return None


# pylint: disable=R0903
class CommonGapFilter:
    """
    Remove common gaps from alignment block
    """

    @staticmethod
    def filter(msa: MultipleSeqAlignment,
               gap_symbol: str = GAP_SYMBOL) -> MultipleSeqAlignment:
        """
        Remove common gaps from alignment block.

        :param msa: <class 'Bio.Align.MultipleSeqAlignment'>
        :param gap_symbol: str
        :return: <class 'Bio.Align.MultipleSeqAlignment'>
        """
        seq_len = len(msa[0].seq)
        j = 0
        while j < seq_len:
            common_gap = True
            for sr in msa:  # sr is of type <class 'Bio.SeqRecord.SeqRecord'>
                if sr[j] != gap_symbol:
                    common_gap = False
                    break
            if common_gap:
                msa = CommonGapFilter. \
                    _remove_symbol(msa, j, gap_symbol)
                seq_len -= 1
            else:
                j += 1
        return msa

    @staticmethod
    def _remove_symbol(msa: MultipleSeqAlignment,
                       j: int,
                       gap_symbol: str) -> MultipleSeqAlignment:
        """
        Remove jth symbol (common gap) from all sequences in alignment.

        Addresses case in which there are *leading* common gaps (this can
        occur when selecting sequences by species). In this case, we need to
        adjust the starting nucleotide address, incrementing by the number of
        leading common gaps.

            start = 1000 ----ATGAGCT

        becomes

            start = 1004 ATGAGCT

        I'm not sure this ^ is correct. TODO Double check this!

        :param msa: <class 'Bio.Align.MultipleSeqAlignment'>
        :param j: int
        :return: <class 'Bio.Align.MultipleSeqAlignment'>
        """
        for sr in msa:  # sr is of type <class 'Bio.SeqRecord.SeqRecord'>
            assert sr[j] == gap_symbol
            sr.seq = sr.seq[:j] + sr.seq[j + 1:]
            if j == 0:
                sr.annotations['start'] += 1
        return msa
