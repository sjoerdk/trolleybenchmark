from pathlib import Path
from typing import List

import pytest
from matplotlib import pyplot as plt

from tests.factories import TrolleyDownloadResultFactory
from trolleybenchmark.experiments import TrolleyDownloadResult
from trolleybenchmark.persistence import Results
from trolleybenchmark.plotting import BoxPlotDataPoint, StringOrdering, \
    boxplot_per_label


@pytest.fixture
def some_results():
    results = []
    for _ in range(10):
        results.append(TrolleyDownloadResultFactory(label="label1"))
    for _ in range(9):
        results.append(TrolleyDownloadResultFactory(label="label2"))

    return Results(description="Test Results",
                   contents=results)


@pytest.fixture
def a_results_file(tmpdir, some_results):
    results_file = Path(tmpdir / "a_results_file.pcl")
    some_results.save(results_file)
    return results_file


def test_plotting(a_results_file):
    """Just don't crash"""
    # plot some data_points file
    results: List[TrolleyDownloadResult] = Results.load(a_results_file).contents
    # convert to data point
    data_points = [BoxPlotDataPoint(
        value=x.mb_per_second, label=x.label) for x in results]
    boxplot_per_label(data_points=data_points, title='test plot')
    # Visually inspect once, then just assume it will work.
    # plt.show()


def test_string_ordering():
    ordering = StringOrdering(first=['one', 'two'], last=['the end'])
    assert ordering.apply(['three', 'two', '']) == ['two', 'three', '']