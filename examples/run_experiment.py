"""Running a WADO-RS download speed benchmark
"""
import logging
from os import environ

import requests
from dicomtrolley.core import StudyReference
from dicomtrolley.qido_rs import QidoRS
from dicomtrolley.trolley import Trolley

from dicomtrolley.wado_rs import WadoRS

from trolleybenchmark.runner import Runner
from trolleybenchmark.experiments import TrolleyDownloadExperiment, \
    WadoRSTrolleyDownloadStudy

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("PIL").setLevel(logging.INFO)  # shut up PIL

session = requests.Session()
trolley = Trolley(downloader=WadoRS(session=session,
                                    url=environ['WADO_RS_URL']),
                  searcher=QidoRS(session=session,
                                  url=environ['WADO_RS_URL']))


studies = [StudyReference('123')]

for study in studies:
        # make sure
        series_list = trolley.ensure_to_series_level([study])

        experiments = []
        for series in series_list:
                experiments.append(TrolleyDownloadExperiment(
                        trolley=trolley,
                        target=series,
                        tmp_dir=f"/tmp/run_experiment/",
                        label=f"series for {study.study_uid}",
                        comment=f"test_comment"))

runner = Runner(experiments=experiments,
                results_path="/tmp/runner")
runner.run()



