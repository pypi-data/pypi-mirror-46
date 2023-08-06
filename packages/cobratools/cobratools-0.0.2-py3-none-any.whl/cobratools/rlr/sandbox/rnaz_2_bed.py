# -*- coding: utf-8 -*-
"""
Extract information from RNAz output and produce BED format output.
"""

import glob
# import sys
import os

from general.models import RNAz

RNAZ_OUT_DIR = './output/06_rnaz_2'
REF_SPECIES = 'mm10'

RNAZ_OUT_LIST = glob.glob(os.path.join(RNAZ_OUT_DIR, '*.out'))


def run():
    """
    Just do it
    """
    d_stats = {'files': 0, 'results': 0, 'probs': []}
    parser = RNAz()
    # lines = []

    for rnaz_out_file in RNAZ_OUT_LIST:
        d_stats['files'] += 1
        records = parser.parse(rnaz_out_file)
        for record in records:
            score = round(float(record['SVM RNA-class probability']) * 100, 4)
            d_stats['probs'].append(score)
            for sequence in record['sequences']:
                if sequence['species'] == REF_SPECIES:
                    data = [sequence['chrom'],
                            str(sequence['start']),
                            str(sequence['end']),
                            sequence['id'],
                            str(score),
                            sequence['strand']]
                    line = '\t'.join(data)
                    # lines.append(line)
                    print(line)


if __name__ == '__main__':
    run()
