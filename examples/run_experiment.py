"""Running a WADO-RS download speed benchmark
"""

import requests

from dicomtrolley.wado_rs import WadoRS

from trolleybenchmark.runner import Runner
from trolleybenchmark.experiments import WadoRSTrolleyDownloadStudy

session = requests.Session()
wado_rs = WadoRS(session=session, url="http://hostname/dicomweb/")


experiment = WadoRSTrolleyDownloadStudy(
        downloader=wado_rs,
        study_uid='1234',
        tmp_dir=f"/tmp/run_experiment/",
        label=f"test_run",
        comment=f"test_comment")

runner = Runner(results_path="/tmp/runner")
runner.run()

