import datetime

from factory import Factory, Sequence
from factory.fuzzy import FuzzyInteger, FuzzyNaiveDateTime, FuzzyFloat
from pydicom import Dataset
from pydicom.tag import Tag

from trolleybenchmark.core import Result
from trolleybenchmark.experiments import TrolleyDownloadResult


class ResultFactory(Factory):
    class Meta:
        model = Result

    comment = Sequence(lambda n: f"comment_{n}")
    label = Sequence(lambda n: f"label_{n}")
    timestamp = FuzzyNaiveDateTime(start_dt=datetime.datetime(2008, 1, 1),
                                   end_dt=datetime.datetime(2023, 1, 1))


class TrolleyDownloadResultFactory(Factory):
    class Meta:
        model = TrolleyDownloadResult

    comment = Sequence(lambda n: f"comment_{n}")
    label = Sequence(lambda n: f"label_{n}")
    timestamp = FuzzyNaiveDateTime(start_dt=datetime.datetime(2008, 1, 1),
                                   end_dt=datetime.datetime(2023, 1, 1))
    duration = FuzzyFloat(0.1, 400.0)
    seconds_total = FuzzyFloat(0.1, 400.0)
    mb_per_second = FuzzyFloat(0.1, 30.0)
    instances_downloaded = FuzzyInteger(2, 3000)


def quick_dataset(*_, **kwargs) -> Dataset:
    """Creates a pydicom dataset with keyword args as tagname - value pairs

    Examples
    --------
    >>> ds = quick_dataset(PatientName='Jane', StudyDescription='Test')
    >>> ds.PatientName
    'Jane'
    >>> ds.StudyDescription
    'Test'

    Raises
    ------
    ValueError
        If any input key is not a valid DICOM keyword

    """
    dataset = Dataset()
    dataset.is_little_endian = True  # required common meta header choice
    dataset.is_implicit_VR = False  # required common meta header choice
    for tag_name, value in kwargs.items():
        Tag(tag_name)  # assert valid dicom keyword. pydicom will not do this.
        dataset.__setattr__(tag_name, value)
    return dataset