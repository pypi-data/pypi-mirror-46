# -*- coding: utf-8 -*-
"""
﻿For aligning up to about 15 sequences of lengths up to a few hundred nt
(like most RNAs in Rfam and as tested in the Bralibase benchmark), a
recommended parametrization is e.g.

mlocarna --probabilistic --consistency-transformation --iterations=2 \
    --max-diff=60 --mea-beta=400 --tgtdir TGT IN.fa

Run this in directory containing RNAz clustered data, e.g.,
locus2	mm10.chr3	3761056	3761159	5	70.49	0.785747	-1.47

NOTE: At present, this script works for SINGLE WINDOW LOCI ONLY. See:
tools/single_window_loci.py
"""

import glob
import os
import sys

TEMPLATE = """#PBS -l nodes=1:ppn=1
#PBS -l walltime=30:00:00
#PBS -N $JOB_NAME
#PBS -M cbcafier@uvm.edu
# Send email only on ABORT
#PBS -m a

spack load perl@5.24.1
cd $HOME/rna_struct/output/04_locarna
echo "This is $JOB_NAME running on " `hostname`
mlocarna --probabilistic --consistency-transformation --iterations=2 --max-diff=60 --mea-beta=400 --dont-plot $DATA_FILE
"""

if __name__ == '__main__':

    IN_PATH = sys.argv[1]
    # print(IN_PATH)
    FILE_LIST = glob.glob(os.path.join(IN_PATH, 'single_window_loci_chr*.dat'))
    # print(FILE_LIST)
    DIRECTIONS = ['fwd', 'rev']
    LOCARNA_DIR = '/users/c/b/cbcafier/rna_struct/output/04_locarna'

    for file_name in FILE_LIST:

        with open(file_name) as ifh:
            line = 'YES'
            while line:
                line = ifh.readline()
                if line.startswith("locus"):
                    tokens = line.split()
                    species = tokens[1].split('.')[0]
                    chromosome = tokens[1].split('.')[1]
                    start = tokens[2]
                    files = []
                    for direction in DIRECTIONS:
                        data_file = species + '.' + chromosome + '_' + start \
                                    + '_' + direction + '.flanked.fa'
                        # outdir_name = species + '.' + chromosome + '_' + start \
                        #             + '_' + direction + '.flanked.out'
                        data_file_path = os.path.join(LOCARNA_DIR, data_file)
                        if os.path.isfile(data_file_path):
                            files.append((data_file_path,
                                          species,
                                          chromosome,
                                          start,
                                          direction))
                    for data_file_path, species, chromosome, start, direction in files:
                        job_name = species + '.' + chromosome + '_' \
                                   + start + '_' + direction
                        script_file = job_name + '.script'
                        script_file_path = os.path.join(LOCARNA_DIR,
                                                        'scripts',
                                                        script_file)

                        print("JOB: {}".format(job_name))
                        print("DATA FILE: {}".format(data_file_path))
                        print("SCRIPT FILE: {}".format(script_file_path))
                        try:
                            with open(script_file_path, "w") as ofh:
                                s = TEMPLATE
                                s = s.replace("$JOB_NAME",
                                              "LOCARNA_" + job_name)
                                s = s.replace("$DATA_FILE", data_file_path)
                                # s = s.replace("$DIR", source_dir)
                                # print(s)
                                ofh.write(s)
                        except IOError:
                            print("*** Unable to open {}".format(
                                script_file_path))
