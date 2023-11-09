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
from dataclasses import field
from typing import Any, Collection, Dict, List

import numpy as np
import matplotlib.pyplot as plt
from pydantic import BaseModel


class BoxPlotDataPoint(BaseModel):
    """A datapoint to put in a boxplot function

    """
    value: float
    label: str       # Main way to distinguish data point class
    bin_name: str = ""         # For multi-group bar charts


class StringOrdering:
    """An ordering for strings

    Made this to say 'this should be first', 'this should be last' while also
    allowing non-defined items to just be put somewhere in the middle using any
    sorting you want
    """
    def __init__(self, first: List[str]= None, last: List[str] = None):
        self.first = first or []
        self.last = last or []

    def ordinal_dict(self):
        """Returns the weights for each string. Undefined = 0. First counts up,
        Last counts down"""

        first_ordinals = {item:idx for idx,item in enumerate(reversed(self.first), start=1)}
        last_ordinals = {item:-idx for idx,item in enumerate(self.last, start=1)}
        return {**first_ordinals,**last_ordinals}

    def apply(self, strings: List[str]) -> List[str]:
        """Apply ordering to this list"""
        ordinal_dict = self.ordinal_dict()

        with_ordinal = []
        for string in strings:
            with_ordinal.append((ordinal_dict.get(string, 0),string))
        return  [x[1] for x in sorted(with_ordinal,key=lambda x: x[0], reverse=True)]

def boxplot_per_label(data_points: Collection[BoxPlotDataPoint], title='title',
                      xlabel='',ylabel='', figsize=(8, 8), label_ordering=None):
    """A horizontal boxplat. Group all data_points by label

    Parameters
    ----------
    label_ordering: StringOrdering, optional
        If this is given, apply this ordering before plotting
    """

    # collect per suid
    per_type = defaultdict(list)
    for data_point in data_points:
        per_type[data_point.label].append(data_point)
    per_type_sorted = {}
    for key in sorted(per_type.keys()):  # sort dict
        per_type_sorted[key] = per_type[key]

    # boxplot per type
    fig, ax = plt.subplots(figsize=figsize)
    if label_ordering:
        bin_sorting = label_ordering.apply(per_type_sorted.keys())
    else:  # sort alphabetically per label
        bin_sorting = sorted(per_type_sorted.keys())
    bins_sorted = [per_type_sorted[x] for x in bin_sorting]

    ax.boxplot([np.array([y.value for y in x]) for x in bins_sorted], vert=False)

    labels = [x[0].label for x in bins_sorted]
    ax.set_yticklabels(labels)
    ax.set(title=title, ylabel=ylabel, xlabel=xlabel)
    ax.grid(True, which='major')
    fig.tight_layout()

    return fig, ax