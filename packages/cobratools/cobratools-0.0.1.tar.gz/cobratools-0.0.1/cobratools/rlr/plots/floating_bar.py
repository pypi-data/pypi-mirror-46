import matplotlib.patches as patches
import matplotlib.pyplot as plt

EXON = '#385789'
TRANSCRIPT = '#3a9b09'
GENE = '#a01e5b'
UTR = '#c15000'
STOP_CODON = '#000000'
START_CODON = '#000000'
CDS = '#2285a3'
SELENOCYSTEINE = '#f6ff0c'


def plot_feature(data, thickness=0.5):
    """
    :param data:
    :param thickness:
    :return:
    """
    yspan = len(data)
    yplaces = [0.5 + i for i in range(yspan)]
    ylabels = sorted(data.keys())

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_yticks(yplaces)
    ax.set_yticklabels(ylabels)
    ax.set_ylim((0, yspan))

    low, hi, color = data[ylabels[0]]
    for pos, label in zip(yplaces, ylabels):
        start, end, color = data[label]
        ax.add_patch(
            patches.Rectangle((start, pos - thickness / 2.0), end - start,
                              thickness, color=color))
        if start < low:
            low = start
        if end > hi:
            hi = end

    # Draw invisible line so that the x axis limits are automatically adjusted
    ax.plot((low, hi), (0, 0))

    ax.grid(axis='x')
    return ax


data = {'L': (29245107, 29253006, GENE),
        'K': (29245107, 29252993, TRANSCRIPT),
        'I': (29250910, 29253006, TRANSCRIPT),
        'H': (29245107, 29248878, EXON),
        'G': (29250910, 29251206, EXON),
        'F': (29251347, 29251459, EXON),
        'E': (29251347, 29252040, EXON),
        'D': (29251461, 29251634, EXON),
        'C': (29251636, 29252040, EXON),
        'B': (29252259, 29253006, EXON),
        'A': (29252465, 29252993, EXON)
        }

ax = plot_feature(data)
ax.set_xlabel('ENSMUSG00000079499.9')
plt.show()
