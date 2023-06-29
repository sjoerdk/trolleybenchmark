from unittest.mock import Mock

import pytest
from dicomtrolley.core import StudyReference
from dicomtrolley.wado_rs import WadoRS

from tests.factories import quick_dataset
from trolleybenchmark.experiments import WadoRSTrolleyDownloadStudy


@pytest.fixture
def a_wado_rs():
    mock = Mock(spec=WadoRS)

    def yield_some_datasets(target):
        yield from [quick_dataset(
            StudyInstanceUID='123',
            SeriesInstanceUID='456',
            SOPInstanceUID=f"1.2.3.{i}") for i in range(10)]
    mock.datasets = yield_some_datasets
    return mock


def test_experiment(a_wado_rs, tmp_path):
    tmp_dir = tmp_path / 'test_experiment'
    tmp_dir.mkdir()

    experiment = WadoRSTrolleyDownloadStudy(downloader=a_wado_rs,
                                            targets=[StudyReference('123')],
                                            tmp_dir=tmp_dir,
                                            label='test',
                                            comment='')
    result = experiment.run()
    assert result  # Just no crash=good currently
