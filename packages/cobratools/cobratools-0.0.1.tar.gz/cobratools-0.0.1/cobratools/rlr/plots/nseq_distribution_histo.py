# -*- coding: utf-8 -*-
from statistics import mean

import matplotlib.pyplot as plt
from general.colors import GRIDLINES, SERIES_1, SERIES_1_EDGE

n_bins = 5

# data = [6] * 10563 + [5] * 2230 + [4] * 991 + [3] * 605 + [2] * 746
data = [6] * 302 + [5] * 101 + [4] * 38 + [3] * 37 + [2] * 63

n = len(data)
mean = round(mean(data), 2)

plt.rc('axes', axisbelow=True)
plt.grid(axis='y', which='major', color=GRIDLINES, linestyle='-')
plt.hist(data, bins=n_bins, color=SERIES_1,
         edgecolor=SERIES_1_EDGE, linewidth=0.2)
plt.ylabel('Alignment blocks')
plt.xlabel("Number of species in alignment\n(n = {}, μ = {})".format(n, mean))
plt.xticks(range(1, 8))
plt.tight_layout()
plt.savefig('nseq_distribution_2.png')
plt.show()

print(24 / float(n))
