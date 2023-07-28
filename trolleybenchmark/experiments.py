"""Specific experiments"""
import dataclasses
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Sequence

from dicomtrolley.core import DICOMDownloadable, StudyReference
from dicomtrolley.storage import StorageDir
from dicomtrolley.trolley import Trolley
from dicomtrolley.wado_rs import WadoRS

from trolleybenchmark.core import Experiment, Result
from trolleybenchmark.logging import get_module_logger
from trolleybenchmark.os_functions import du, format_bytes
from trolleybenchmark.persistence import Results
from trolleybenchmark.timing import TrolleyDownloadTimer

logger = get_module_logger('experiments')


class TrolleyDownloadResult(Result):
    seconds_total: float
    bytes_downloaded: int
    mb_per_second: float
    instances_downloaded: int



class TrolleyDownloadExperiment(Experiment):
    """Time how long it takes to download a single target"""

    def __init__(self, trolley:Trolley, target: DICOMDownloadable,
                 tmp_dir: str, label: str, comment: str, limit: int = 0):
        super().__init__(label=label, comment=comment)
        self.tmp_dir = tmp_dir
        self.trolley = trolley
        self.target: DICOMDownloadable = target
        self.limit = limit

    @staticmethod
    def empty_dir(folder):
        if Path(folder).exists():
            logger.info(f'removing all data in {folder}')
            shutil.rmtree(folder)

    def run(self) -> TrolleyDownloadResult:

        count = 0
        start = datetime.now()
        timer = TrolleyDownloadTimer()
        timer.attach_to_trolley(self.trolley)

        self.trolley.download(objects=[self.target], output_dir=self.tmp_dir)
        end = datetime.now()
        duration = (end-start).total_seconds()
        bytes_on_disk = du(self.tmp_dir)
        logger.info(
            f'{bytes_on_disk} bytes downloaded ({format_bytes(bytes_on_disk)}) '
            f'in {(duration):.2f}s')

        mb_per_second = (bytes_on_disk / duration) / (1024 ** 2)
        instances_downloaded = count
        self.empty_dir(self.tmp_dir)

        tags = {'target': dataclasses.asdict(self.target.reference()),
                'downloader': str(self.trolley.downloader),
                'searcher': str(self.trolley.searcher),
                'timer_total': timer.total_time,
                'timer_search': timer.search_time,
                'timer_download': timer.download_time}

        return TrolleyDownloadResult(label=self.label,
                                     comment=self.comment,
                                     tags=tags,
                                     timestamp=start,
                                     bytes_downloaded=bytes_on_disk,
                                     seconds_total=(end - start).total_seconds(),
                                     mb_per_second=mb_per_second,
                                     instances_downloaded=instances_downloaded)


class WadoRSTrolleyDownloadStudy(Experiment):
    """Time how long it takes to download targets"""

    def __init__(self, downloader: WadoRS, target: DICOMDownloadable,
                 tmp_dir: str, label: str, comment: str, limit: int = 0):
        super().__init__(label=label, comment=comment)
        self.tmp_dir = tmp_dir
        self.storage = StorageDir(tmp_dir)
        self.downloader = downloader
        self.target: DICOMDownloadable = target
        self.limit = limit

    def run(self) -> TrolleyDownloadResult:
        """Get default params for result, and then collect stuff"""

        if Path(self.tmp_dir).exists():
            logger.info(f'removing all data in {self.tmp_dir}')
            shutil.rmtree(self.tmp_dir)

        count = 0
        start = datetime.now()
        for count, dataset in enumerate(
                self.downloader.datasets(self.target)):
            if self.limit and count >= self.limit:
                logger.info(f'Stopping after downloading {self.limit} slices')
                break
            self.storage.save(dataset=dataset)
        end = datetime.now()
        duration = (end-start).total_seconds()
        bytes_on_disk = du(self.tmp_dir)
        logger.info(
            f'{bytes_on_disk} bytes downloaded ({format_bytes(bytes_on_disk)}) '
            f'in {(duration):.2f}s')

        mb_per_second = (bytes_on_disk / duration) / (1024 ** 2)
        instances_downloaded = count

        return TrolleyDownloadResult(label=self.label,
                                     comment=self.comment,
                                     tags=dataclasses.asdict(self.target.reference()),
                                     timestamp=start,
                                     bytes_downloaded=bytes_on_disk,
                                     seconds_total=(end - start).total_seconds(),
                                     mb_per_second=mb_per_second,
                                     instances_downloaded=instances_downloaded)


class TrolleyDownloadResults(Results):
    """Contains data_points. For easy persisting"""
    contents: List[TrolleyDownloadResult]
