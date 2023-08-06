# -*- coding: utf-8 -*-
"""
Common stuff
"""

from cobratools.general.models.constants import NORMAL_DIRECTION_SYMBOL, \
    REVERSE_COMPLIMENT_SYMBOL


# pylint: disable=R0903
class StrandAware:
    """
    Mixin base class for strand-aware classes
    """

    @staticmethod
    def get_strand(x):
        """
        Be tolerant of how strand is annotated +/1, - /0
        :param x:
        :return:
        """
        if x in [1, NORMAL_DIRECTION_SYMBOL]:
            return NORMAL_DIRECTION_SYMBOL
        if x in [0, REVERSE_COMPLIMENT_SYMBOL]:
            return REVERSE_COMPLIMENT_SYMBOL
        return NORMAL_DIRECTION_SYMBOL
