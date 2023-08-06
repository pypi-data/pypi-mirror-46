# -*- coding: utf-8 -*-
"""
BED file stuff
"""


# pylint: disable=R0902,R0903
class BedLine:
    """
    A line of a BED file
    """

    def __init__(self, d):
        """
        Init
        {'chrom': None,
         'chromStart': None,
         'chromEnd': None,
         'name': None,
         'score': None,
         'strand': None,
         'thickStart': None,
         'thickEnd': None,
         'itemRgb': None,
         'blockCount': None,
         'blockSizes': None,
         'blockStarts': None}
        :param d: dict
        """
        self.chrom = d['chrom']
        self.chrom_start = int(d['chromStart'])
        self.chrom_end = int(d['chromEnd'])
        self.name = d['name']
        self.score = self._set_score(d)
        self.strand = self._set_strand(d)
        self.thick_start = self._set_thick_start(d)
        self.thick_end = self._set_thick_end(d)
        self.item_rgb = self._set_item_rgb(d)
        self.block_count = self._set_block_count(d)
        self.block_sizes = self._set_block_sizes(d)
        self.block_starts = self._set_block_starts(d)

    @staticmethod
    def _set_score(d):
        """

        :param d:
        :return:
        """
        if d['score'] is not None:
            return float(d['score'])
        return None

    @staticmethod
    def _set_strand(d):
        """

        :param d:
        :return:
        """
        if d['strand'] is not None:
            if d['strand'] in [1, '1', '+']:
                return '+'
            return '-'
        return None

    @staticmethod
    def _set_thick_start(d):
        """

        :param d:
        :return:
        """
        if d['thickStart'] is not None:
            return int(d['thickStart'])
        return None

    @staticmethod
    def _set_thick_end(d):
        """

        :param d:
        :return:
        """
        if d['thickStart'] is not None and d['thickEnd'] is not None:
            return int(d['thickEnd'])
        return None

    @staticmethod
    def _set_item_rgb(d):
        """

        :param d:
        :return:
        """
        if d['itemRgb'] is not None:
            rgb = [int(x) for x in d['itemRgb'].split(',')]
            if len(rgb) == 3:
                return rgb
        return None

    @staticmethod
    def _set_block_count(d):
        """

        :param d:
        :return:
        """
        if d['blockCount'] is not None:
            return int(d['blockCount'])
        return None

    @staticmethod
    def _set_block_sizes(d):
        """

        :param d:
        :return:
        """
        if d['blockCount'] is not None and d['blockSizes'] is not None:
            sizes = [int(x) for x in d['blockSizes'].split(',')]
            if len(sizes) == int(d['blockCount']):
                return sizes
        return None

    @staticmethod
    def _set_block_starts(d):
        """

        :param d:
        :return:
        """
        if d['blockCount'] is not None and d['blockStarts'] is not None:
            starts = [int(x) for x in d['blockStarts'].split(',')]
            if len(starts) == int(d['blockCount']):
                return starts
        return None

    def __str__(self):
        """
        TODO incomplete
        :return:
        """
        tokens = [self.chrom,
                  str(self.chrom_start),
                  str(self.chrom_end)]
        if self.name is not None:
            tokens.append(self.name)
            if self.score is not None:
                tokens.append(str(self.score))
                if self.strand is not None:
                    tokens.append(self.strand)
        return '\t'.join(tokens)
