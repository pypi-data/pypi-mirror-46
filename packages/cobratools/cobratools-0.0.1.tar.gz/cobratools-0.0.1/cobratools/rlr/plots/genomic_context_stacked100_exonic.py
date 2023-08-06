# libraries

# import numpy as np
import matplotlib.pyplot as plt
# from matplotlib import rc
import pandas as pd

# Data
r = [0, 1, 2, 3, 4]
raw_data = {'coding': [56.0, 44.0, 73.5, 64.4, 69.2],
            'non_coding': [20.0, 32.0, 7.6, 19.2, 13.1],
            'other': [24.0, 24.5, 18.9, 16.4, 17.6]}
df = pd.DataFrame(raw_data)

# From raw value to percentage
totals = [i + j + k for i, j, k in
          zip(df['coding'], df['non_coding'], df['other'])]
coding = [i / j * 100 for i, j in zip(df['coding'], totals)]
non_coding = [i / j * 100 for i, j in zip(df['non_coding'], totals)]
other = [i / j * 100 for i, j in zip(df['other'], totals)]

# plot
barWidth = 0.85
names = ('Theil input\nalignments', 'Thiel RNAz hits', 'Our input\nalignments',
         'Our RNAz hits', 'Our hits not\nin Thiel HC')
# Create green Bars
plt.bar(r, coding, color='#4ba209', edgecolor='white', width=barWidth)
# Create orange Bars
plt.bar(r, non_coding, bottom=coding, color='#4dac61', edgecolor='white',
        width=barWidth)
# Create blue Bars
plt.bar(r, other, bottom=[i + j for i, j in zip(coding, non_coding)],
        color='#4aaf9e', edgecolor='white', width=barWidth)

# Custom x axis
plt.xticks(r, names)
plt.xlabel("Exonic (coding vs non-coding vs other)")
plt.ylabel("Proportional coverage (%)")

# Show graphic
plt.show()
