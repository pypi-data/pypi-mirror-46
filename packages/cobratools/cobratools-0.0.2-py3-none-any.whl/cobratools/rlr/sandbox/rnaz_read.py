# -*- coding: utf-8 -*-
"""
Read from RNAz output file. This is really a test / sandbox item.
"""

from general.models import RNAz


def run():
    """
    Just do it
    """
    rnaz = RNAz()
    rnaz.parse('./tests/data/test-rnaz.out')


if __name__ == '__main__':
    run()
