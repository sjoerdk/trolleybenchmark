"""Specific experiments"""
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Sequence

from dicomtrolley.core import DICOMDownloadable, StudyReference
from dicomtrolley.storage import StorageDir
from dicomtrolley.wado_rs import WadoRS

from trolleybenchmark.core import Experiment, Result
from trolleybenchmark.logging import get_module_logger
from trolleybenchmark.os_functions import du, format_bytes
from trolleybenchmark.persistence import Results

logger = get_module_logger('experiments')


class TrolleyDownloadResult(Result):
    seconds_total: float
    mb_per_second: float
    instances_downloaded: int


class WadoRSTrolleyDownloadStudy(Experiment):
    """Time how long it takes to download targets"""

    def __init__(self, downloader: WadoRS, targets: Sequence[DICOMDownloadable],
                 tmp_dir: str, label: str, comment: str, limit: int=0):
        super().__init__(label=label, comment=comment)
        self.tmp_dir = tmp_dir
        self.storage = StorageDir(tmp_dir)
        self.downloader = downloader
        self.targets = targets
        self.limit = limit

    def run(self) -> TrolleyDownloadResult:
        # get default params for result, and then collect stuff

        if Path(self.tmp_dir).exists():
            logger.info(f'removing all data in {self.tmp_dir}')
            shutil.rmtree(self.tmp_dir)

        count = 0
        start = datetime.now()
        for count, dataset in enumerate(
                self.downloader.datasets(self.targets)):
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
                                     comment='',
                                     timestamp=start,
                                     seconds_total=(end - start).total_seconds(),
                                     mb_per_second=mb_per_second,
                                     instances_downloaded=instances_downloaded)


class TrolleyDownloadResults(Results):
    """Contains results. For easy persisting"""
    contents: List[TrolleyDownloadResult]
