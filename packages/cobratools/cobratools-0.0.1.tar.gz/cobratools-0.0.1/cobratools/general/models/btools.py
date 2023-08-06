# -*- coding: utf-8 -*-
"""
A thin convenience wrapper around selected Bedtools functions for use here.
"""

import os

# pylint: disable = E0401
import pybedtools
from pybedtools.helpers import BEDToolsError

from cobratools.general.config import CONF  # TODO doesn't belong here!
from cobratools.general.models.alphabets import TRANS_T2U
from cobratools.general.models.constants import GAP_SYMBOL, NORMAL_DIRECTION_SYMBOL, \
    REVERSE_COMPLIMENT_SYMBOL


class Bedtools:
    """
    A thin convenience wrapper around selected Bedtools functions for use here.
    """

    @staticmethod
    def get_fasta(species, chrom, start, end, direction):
        """
        Fetch data from FASTA file using Bedtools

        :param species:
        :param chrom:
        :param start:
        :param end:
        :param direction:
        :return:
        """
        if direction == NORMAL_DIRECTION_SYMBOL:
            descr = 'fwd'
        elif direction == REVERSE_COMPLIMENT_SYMBOL:
            descr = 'rvc'
        else:
            raise Exception("Invalid or missing direction (strand)")
        genome_file = os.path.join(CONF['GENOME_DATA_PATH'],
                                   species, chrom + '.fa')
        s = "\t".join([chrom, str(start), str(end), descr, "1", direction])
        a = pybedtools.BedTool(s, from_string=True)
        try:
            fasta = pybedtools.example_filename(genome_file)
            a = a.sequence(fi=fasta, s=True)  # s=True strand
            with open(a.seqfn, "r") as fh2:
                lines = fh2.readlines()
                assert not lines[1].startswith('>')
                s = lines[1].translate(TRANS_T2U)
            return s.strip()
        except BEDToolsError as err:
            print('PyBedTools error {}'.format(str(err)))
            return ''
        except FileNotFoundError:
            # print("--------------------------------------------------")
            print("{} file not found".format(genome_file))
            return ''

    @staticmethod
    def verify_fasta(sr, reference, softmask_ok=True):
        """
        Verify by comparing sequence and result from fetched FASTA data

        :param sr:
        :param reference:
        :param softmask_ok:
        :return:
        """
        # species, chrom, start, end, direction
        species = sr.id.split('.')[0]
        chrom = sr.id.split('.')[1]
        start = sr.annotations['start']
        size = sr.annotations['size']
        # NOTE: BioPython documentation says that annotation for strand is an
        # enum("+", "-"), but in fact this is wrong. I'm seeing 1 = normal,
        # 0 = rev. complement. So we support both (maybe they'll fix someday).
        # See: https://biopython.org/wiki/Multiple_Alignment_Format
        direction = NORMAL_DIRECTION_SYMBOL
        if sr.annotations['strand'] in [1, NORMAL_DIRECTION_SYMBOL]:
            direction = NORMAL_DIRECTION_SYMBOL
        if sr.annotations['strand'] in [0, REVERSE_COMPLIMENT_SYMBOL]:
            direction = REVERSE_COMPLIMENT_SYMBOL
        end = start + size
        try:
            assert end > start
        except AssertionError:
            print("--------------------------------------------------")
            print("Bad size: {}.{} {} {} {}".format(species,
                                                    chrom,
                                                    start,
                                                    size,
                                                    direction))
            print("Reference = {}".format(reference))

        from_fa = Bedtools.get_fasta(species, chrom, start, end, direction)
        ok, actual = Bedtools.compare(from_fa, str(sr.seq))
        # if ok:
        #     return ok, actual
        # print("--------------------------------------------------")
        # print("Failed match: {}.{} {} {} {}".format(species,
        #                                             chrom,
        #                                             start,
        #                                             size,
        #                                             direction))
        # print("Fetched from genome: {}".format(actual))
        # print("Input sequence:      {}".format(str(sr.seq)))
        # print("Reference = {}".format(reference))
        return ok, actual

    @staticmethod
    def compare(act, exp, softmask_ok=True):
        """
        Compare two strings, excluding gaps
        :param act: str
        :param exp: str
        :param softmask_ok: bool
        :return: bool, str
        """
        try:
            actual = act.replace(GAP_SYMBOL, '')
            expected = exp.replace(GAP_SYMBOL, '').translate(TRANS_T2U)
            if softmask_ok:
                assert actual.upper() == expected.upper()
            else:
                assert actual == expected
            return True, actual
        except AssertionError:
            # print("Expected {}".format(expected))
            # print("  Actual {}".format(actual))
            # noinspection PyUnboundLocalVariable
            return False, actual
