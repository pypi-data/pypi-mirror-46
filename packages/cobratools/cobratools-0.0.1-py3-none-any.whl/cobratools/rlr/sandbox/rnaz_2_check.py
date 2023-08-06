# -*- coding: utf-8 -*-
"""
Did any jobs get skipped? If there's a script and no output, tell me!
"""

import glob
import os
import sys


def run(inpath):
    """
    Just do it
    """
    print(inpath)

    for filename in glob.glob(os.path.join(inpath, '*.script')):
        root, _ = os.path.splitext(filename)
        job_out_filespec = root + '.o*'
        x = glob.glob(job_out_filespec)
        if not x:
            print(filename)


if __name__ == '__main__':
    INPATH = sys.argv[1]
    run(INPATH)
