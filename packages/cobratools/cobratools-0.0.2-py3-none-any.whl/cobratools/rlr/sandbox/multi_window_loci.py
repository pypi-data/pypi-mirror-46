# -*- coding: utf-8 -*-
"""
Select multi window loci in RNAz results

locus1	mm10.chr3	3748045	3748158	5	78.18	0.849477	-2.03
window1	locus1	mm10.chr3	3748045	3748158	-	5	113	78.18	-30.52	...
locus2	mm10.chr3	3760617	3760772	2	98.33	0.992183	-2.84
window2	locus2	mm10.chr3	3760617	3760737	+	2	120	98.33	-25.70	...
window3	locus2	mm10.chr3	3760617	3760737	-	2	120	98.33	-33.15	...
window4	locus2	mm10.chr3	3760637	3760757	+	2	120	97.50	-33.10	...
window5	locus2	mm10.chr3	3760652	3760772	+	2	120	95.83	-32.70	...
window6	locus2	mm10.chr3	3760652	3760772	-	2	120	95.83	-29.25	...

"""

import sys


def run(infile):
    """
    Just do it
    """
    tmp = []
    with open(infile, "r") as fh:
        count_windows = 0
        line = True
        while line:
            line = fh.readline()
            if line.startswith("locus"):
                if count_windows > 1:
                    for x in tmp:
                        print(x)
                tmp = []
                count_windows = 0
                tmp.append(line.strip())
            else:
                # Line starts with "window"
                count_windows += 1
                tmp.append(line.strip())


if __name__ == '__main__':
    INFILE = sys.argv[1]
    run(INFILE)
