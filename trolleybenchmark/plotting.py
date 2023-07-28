"""Classes and functions for plotting data_points

The approach is to define simple data structures for data points that can
then be plotted in plotting functions. I considered whether this was overkill and
or superfluous, as matplotlib should in principle already have this. However,
in my experience, whenever I just want to plot 'something like that plot I made
6 months ago' I have to go way too deep into pandas (how do you init a dataframe from
a dict again? Or do I need a Series? What was the difference? Which axis goes where?
How do you transpose a Series? What is an index column?) and matplotlib (how do
you invert the axes? Why are my labels so weird? et cetera).

The hope is that this lib will avoid that annoyance. Time will tell.
"""

from collections import defaultdict
from typing import Collection

import numpy as np
import matplotlib.pyplot as plt
from pydantic.dataclasses import dataclass


@dataclass
class BoxPlotDataPoint:
    """A datapoint to put in a boxplot function

    """
    value: float
    label: str       # Main way to distinguish data point class
    bin_name: str = ""         # For multi-group bar charts


def boxplot_per_label(data_points: Collection[BoxPlotDataPoint], title='title',
                      xlabel='',ylabel='', figsize=(8, 8)):
    """Plot data points in a boxplot. Group all data_points by label"""

    # collect per suid
    per_type = defaultdict(list)
    for data_point in data_points:
        per_type[data_point.label].append(data_point)
    per_type_sorted = {}
    for key in sorted(per_type.keys()):  # sort dict
        per_type_sorted[key] = per_type[key]

    # boxplot per type
    fig, ax = plt.subplots(figsize=figsize)
    bins_sorted = [per_type_sorted[x] for x in sorted(per_type_sorted.keys())]
    ax.boxplot([np.array([y.value for y in x]) for x in bins_sorted], vert=False)

    labels = [x[0].label for x in bins_sorted]
    ax.set_yticklabels(labels)
    ax.set(title=title, ylabel=ylabel, xlabel=xlabel)
    ax.grid(True, which='major')
    fig.tight_layout()

    return fig, ax