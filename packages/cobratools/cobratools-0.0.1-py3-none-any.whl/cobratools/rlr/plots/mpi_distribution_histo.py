# -*- coding: utf-8 -*-
"""

Extract MPIs from RNAz output, thus:

cat output/07_annotation/rnaz_1_combined.out | grep "Mean pairwise identity" | awk '{print $4'} > mpi_rnaz_1.txt

"""

import sys
from statistics import mean

from general import colors as colors
import matplotlib.pyplot as plt
import numpy as np


def read_data(fn):
    """
    Get data from file
    :return:
    """
    data = []
    with open(fn, 'r') as fh:
        datum = True
        while datum:
            datum = fh.readline().strip()
            if datum:  # Ignore blank lines
                data.append(float(datum))
    return data


def get_stats(data):
    n = len(data)
    m = round(mean(data), 2)
    s = None  # placeholder for stdev
    return n, m, s


def make_plot(data, n, m, n_bins):
    plt.rc('axes', axisbelow=True)
    plt.grid(axis='y', which='major', color=colors.GRIDLINES, linestyle='-')
    # plt.hist(data, bins=np.arange(min(data), max(data) + binwidth, binwidth))
    n_bins = np.arange(min(data), max(data), 5)
    plt.hist(data, bins=n_bins, color=colors.SERIES_1,
             edgecolor=colors.SERIES_1_EDGE, linewidth=0.2)
    plt.ylabel('Alignment blocks')
    plt.xlabel("Mean pairwise identity (MPI) x 100\n(n = {}, μ = {})"
               .format(n, m))
    plt.xticks(range(0, 110, 10))
    plt.tight_layout()
    return plt


if __name__ == '__main__':
    input_file = sys.argv[1]
    num_bins = int(sys.argv[2])
    output_image = sys.argv[3]
    data = read_data(input_file)
    n, m, s = get_stats(data)
    plt = make_plot(data, n, m, num_bins)
    plt.savefig(output_image)
    plt.show()
