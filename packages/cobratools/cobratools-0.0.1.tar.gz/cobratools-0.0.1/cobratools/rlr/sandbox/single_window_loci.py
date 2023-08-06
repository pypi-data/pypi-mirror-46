# -*- coding: utf-8 -*-
"""
Select single window loci in RNAz results
"""

import sys


def run(infile):
    """
    Just do it
    """
    loci = []
    tmp = ''
    with open(infile, "r") as fh:
        line = True
        count_windows = 0
        while line:
            line = fh.readline()
            if not line.startswith("window"):
                if count_windows == 1:
                    # Then we have a one-window locus
                    loci.append(tmp)
                tmp = line.strip()
                count_windows = 0
            else:
                count_windows += 1
    for locus in loci:
        print(locus)


if __name__ == '__main__':
    INFILE = sys.argv[1]

    run(INFILE)
