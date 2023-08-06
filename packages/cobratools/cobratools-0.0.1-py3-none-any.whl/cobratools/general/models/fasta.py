# -*- coding] = utf-8 -*-
"""
FASTA stuff
"""


# pylint: disable=R0903
class Fasta:
    """
    For parsing FASTA file
    """

    @staticmethod
    def parse_info_line(l):
        """
        Parse info line into dict
        :param l:
        :return:
        """
        d = {}
        tokens = l.split()
        d['id'] = tokens[0][1:]  # Lop off leading ">"
        try:
            d['species'] = tokens[0].split('.')[0][1:]  # Lop off leading ">"
            d['chrom'] = tokens[0].split('.')[1]
        except IndexError:
            d['species'] = None
            d['chrom'] = None
        if len(tokens) > 1:
            d['start'] = int(tokens[1])
            d['size'] = int(tokens[2])
            d['strand'] = tokens[3]
            d['src_size'] = int(tokens[4])
            d['end'] = d['start'] + d['size']
        return d
