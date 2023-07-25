"""Classes and functions to time specific parts of trolley performance

"""
import time
from functools import wraps


class Timer:
    seconds: float = 0.0

    def reset(self):
        self.seconds = 0.0


def add_timer(func_in, timer: Timer):
    """Log the time spent in function to the given timer object"""
    @wraps(func_in)
    def timed(*args, **kwargs):
        start = time.perf_counter()
        result = func_in(*args, **kwargs)
        timer.seconds += (time.perf_counter() - start)
        return result

    return timed


class TrolleyDownloadTimer:
    """Measures trolley time spent on download and additional queries

    Computes download time by subtracting search from total because download
    uses yield statements that are hard to wrap
    """
    def __init__(self):

        self.search_timer = Timer()
        self.total_timer = Timer()

    def reset(self):
        self.search_timer.reset()
        self.total_timer.reset()

    @property
    def search_time(self):
        return self.search_timer.seconds

    @property
    def total_time(self):
        return self.total_timer.seconds

    @property
    def download_time(self):
        return self.total_time - self.search_time

    def attach_to_trolley(self, trolley):
        """attach monitoring hooks to distinguish search for download time"""

        trolley.ensure_to_series_level = add_timer(
            trolley.ensure_to_series_level, timer=self.search_timer)
        trolley.convert_to_instances = add_timer(
            trolley.convert_to_instances, timer=self.search_timer)
        trolley.download = add_timer(trolley.download, timer=self.total_timer)
