# -*- coding: utf-8 -*-
"""
Did any jobs get skipped? If there's a script and no output, tell me!

For every

mm10.chr1_55447221_rev.flanked.fa.script

there should be a

mm10.chr1_55447221_rev.flanked.out

"""

import glob
import os
import sys

if __name__ == '__main__':

    IN_PATH = sys.argv[1]
    print(IN_PATH)

    TARGET = os.path.join(IN_PATH, 'scripts/*.script')
    print(TARGET)

    for filename in glob.glob(TARGET):
        name, ext = os.path.splitext(os.path.basename(filename))
        job_out_filespec = name + '.flanked.out'
        # print(job_out_filespec)
        x = glob.glob(os.path.join(IN_PATH, job_out_filespec))
        if not x:
            print(filename)
