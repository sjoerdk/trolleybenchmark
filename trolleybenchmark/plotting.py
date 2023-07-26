from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

from trolleybenchmark.experiments import TrolleyDownloadResults
from trolleybenchmark.os_functions import format_bytes


def boxplot_per_label(results: TrolleyDownloadResults, title='title'):
    """Plot download speed for all results with the same label together

    """

    # collect per suid
    per_type = defaultdict(list)
    for result in results.contents:
        per_type[result.label].append(result)
    per_type_sorted = {}
    for key in sorted(per_type.keys()):  # sort dict
        per_type_sorted[key] = per_type[key]

    # boxplot per type
    fig, ax = plt.subplots(figsize=(16, 16))
    bins_sorted = [per_type_sorted[x] for x in sorted(per_type_sorted.keys())]
    ax.boxplot([np.array([y.mb_per_second for y in x]) for x in bins_sorted])

    labels = [x[0].label for x in bins_sorted]
    ax.set_xticklabels(labels)
    ax.set(title=title, xlabel='label', ylabel='Download speed (Mb/s)')
    ax.grid(True, which='major')
    fig.tight_layout()

    return fig, ax