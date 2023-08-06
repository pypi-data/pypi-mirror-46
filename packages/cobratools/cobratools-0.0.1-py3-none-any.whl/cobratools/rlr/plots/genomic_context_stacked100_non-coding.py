# libraries

# import numpy as np
import matplotlib.pyplot as plt
# from matplotlib import rc
import pandas as pd

# Data
r = [0, 1, 2, 3, 4]
raw_data = {'lncRNA': [97.0, 63.4, 99, 87, 93],
            'sncRNA': [3.0, 36.6, 1, 13, 7]}
df = pd.DataFrame(raw_data)

# From raw value to percentage
totals = [i + j for i, j in
          zip(df['lncRNA'], df['sncRNA'])]
lnc_rna = [i / j * 100 for i, j in zip(df['lncRNA'], totals)]
snc_rna = [i / j * 100 for i, j in zip(df['sncRNA'], totals)]

# plot
barWidth = 0.85
names = ('Theil input\nalignments', 'Thiel RNAz hits', 'Our input\nalignments',
         'Our RNAz hits', 'Our hits not\nin Thiel HC')
# Create green Bars
plt.bar(r, lnc_rna, color='#be6bf6', edgecolor='white', width=barWidth)
# Create orange Bars
plt.bar(r, snc_rna, bottom=lnc_rna, color='#df5fcc', edgecolor='white',
        width=barWidth)

# Custom x axis
plt.xticks(r, names)
plt.xlabel("Non-coding (lncRNA vs sncRNA)")
plt.ylabel("Proportional coverage (%)")

# Show graphic
plt.show()
