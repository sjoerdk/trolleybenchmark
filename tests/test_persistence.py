from io import BytesIO

from tests.factories import ResultFactory
from trolleybenchmark.persistence import Results


def test_results_load_save():
    """You can persist data_points to disk"""
    results = Results(contents=[ResultFactory() for _ in range(5)])
    file = BytesIO()
    results.save(file)
    file.seek(0)
    loaded = Results.load(file)

    for old, new in zip(results.contents, loaded.contents):
        assert old == new

