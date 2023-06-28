from pathlib import Path

import pytest
from matplotlib import pyplot as plt

from tests.factories import TrolleyDownloadResultFactory
from trolleybenchmark.persistence import Results
from trolleybenchmark.plotting import boxplot_per_label


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
    # plot some results file
    results = Results.load(a_results_file)
    boxplot_per_label(results=results, title='test plot')
    # Visually inspect once, then just assume it will work.
    # plt.show()
