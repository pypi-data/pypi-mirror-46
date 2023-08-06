import glob
import os
import re
import shutil

if __name__ == '__main__':

    r = re.compile(r'.*.chr[0-9]+_([0-9]+)\.flanked\.out')

    single_window_file = './output/03_preprocessing/results_chr3_single_window.dat'
    locarna_out_dir = './output/04_locarna/chr3_flanked'

    locarna_out_list = glob.glob(os.path.join(locarna_out_dir, '*.out'))
    locarna_iterator = iter(locarna_out_list)

    single_locus_starts = []
    with open(single_window_file) as fh:
        line = True
        while line:
            line = fh.readline()
            if line.startswith("locus"):
                tokens = line.split()
                start = int(tokens[2])
                single_locus_starts.append(start)

    for locarna_output in locarna_out_list:
        m = r.search(locarna_output)
        locarna_start = int(m.group(1))
        if locarna_start not in single_locus_starts:
            shutil.rmtree(locarna_output)
