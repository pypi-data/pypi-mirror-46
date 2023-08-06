# -*- coding: utf-8 -*-
"""
Intersect our BED file (RNAz second run output) with theirs
"""

import glob
# import sys
import os
import subprocess

ANNOTATION_OUT_DIR = './output/07_annotation'

DATA_DIR = './data/RNAz_mm10_trackhub'
BED_FILE = './output/07_annotation/rnaz_2_removed_alt_strands.bed'

TRACKHUB_LIST = glob.glob(os.path.join(DATA_DIR, '*_all.bed6plus6'))
# ./data/RNAz_mm10_trackhub/hc_loci_all_6to10.bed6plus6

if __name__ == '__main__':
    for trackhub_file in TRACKHUB_LIST:
        filename, file_extension = os.path.splitext(trackhub_file)
        filename = filename.split('/')[-1:][0]
        print("------------------------ {} ------------------------"
              .format(trackhub_file))
        args = ['bedtools',
                'intersect',
                '-a',
                BED_FILE,
                '-b',
                trackhub_file]
        proc = subprocess.run(args,
                              encoding='utf-8',
                              stdout=subprocess.PIPE)
        for line in proc.stdout.split('\n'):
            print(line)
