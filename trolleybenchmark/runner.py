from pathlib import Path
from typing import Sequence

from trolleybenchmark.core import Experiment
from trolleybenchmark.logging import get_module_logger
from trolleybenchmark.persistence import Results

logger = get_module_logger("runner")


class Runner:
    """Runs experiments, saves to file"""

    def __init__(self, experiments: Sequence[Experiment], results_path: str):
        self.experiments = experiments
        self.results_path = Path(results_path)

    def run(self):
        logger.info(f'starting run of {len(self.experiments)} results, writing '
                    f'to {self.results_path}')
        try:
            results = Results.load(self.results_path)
            logger.info(f"{self.results_path} existed. Loaded {len(results.contents)} "
                        f"results. Appending to this")
        except FileNotFoundError:
            logger.info(
                f"{self.results_path} did not exist. Starting new results")
            results = Results(contents=[])

        for count, experiment in enumerate(self.experiments):
            logger.info(f'running experiment {count}:{experiment}')
            try:
                results.contents.append(experiment.run())
            except Exception as e:
                logger.exception(e)
                raise
            logger.info(f'saving intermediate results to {self.results_path}')
            results.save(self.results_path)
        logger.info('run finished')
