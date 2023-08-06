# -*- coding] = utf-8 -*-
"""
MAF stuff
"""

from cobratools.general.models.alphabets import TRANS_T2U
from cobratools.general.models.btools import Bedtools
from cobratools.general.models.common import StrandAware
from cobratools.general.models.constants import GAP_SYMBOL


class Maf(StrandAware):
    """
    For parsing MAF files
    """

    @staticmethod
    def parse_line(l):
        """
        Parse line into dict; with some transformations
        :param l:
        :return:
        """
        d = {}
        # That 's' is the first token
        tokens = l.split()
        d['id'] = tokens[1]
        d['species'] = tokens[1].split('.')[0]
        d['chrom'] = tokens[1].split('.')[1]
        d['start'] = int(tokens[2])
        d['size'] = int(tokens[3])
        d['strand'] = Maf.get_strand(tokens[4])
        d['src_size'] = int(tokens[5])
        d['seq'] = tokens[6].translate(TRANS_T2U)
        d['end'] = d['start'] + d['size']
        return d

    @staticmethod
    def maf_verify(filepath):
        """
        Verify MAF data against genome data
        This works, but it's hopelessly slow. Every line in the sequence, we go
        back to genome file and scan through the file.
        """
        mismatches = 0
        with open(filepath, "r") as fh:
            for line in fh:
                # print(line)
                if line.startswith('s '):
                    # That 's' is the first token
                    d = Maf.parse_line(line)
                    from_fa = Bedtools.get_fasta(d['species'], d['chrom'],
                                                 d['start'], d['end'],
                                                 d['strand'])
                    ok, actual = Bedtools.compare(from_fa, d['seq'])
                    if not ok:
                        mismatches += 1
                        ungapped = d['seq'].replace(GAP_SYMBOL, '')
                        print(
                            "----------------------------------------------")
                        print(
                            "Failed match: {}.{} {} {} {}".format(d['species'],
                                                                  d['chrom'],
                                                                  d['start'],
                                                                  d['size'],
                                                                  d['strand']))
                        print("Fetched from genome: {}".format(actual))
                        print("Input sequence:      {}".format(ungapped))
                        print("Reference = {}".format(filepath))
        return mismatches
