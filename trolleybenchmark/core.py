import socket
from datetime import datetime
from pydantic import BaseModel

from trolleybenchmark.logging import get_module_logger

logger = get_module_logger("core")


class Experiment:
    """A piece of code you can execute in a runner to time it and collect results"""

    def __init__(self, comment: str, label: str):
        self.comment = comment
        self.label = label

    def run(self, **kwargs) -> "Result":
        """Run this experiment"""
        raise NotImplementedError

    def get_default_result_args(self):
        """Default values for base Result parameters

        Saves boiler plate in implementing classes.

        Example
        -------
        class MyResult(Result):
            my_new_var: str

        class MyExperiment(Experiment):
            def run():

                MyResult(my_var=value,**self.get_default_result_args()))

        """
        return {"comment": self.comment,
                "label": self.label,
                "timestamp": datetime.now(),
                "hostname": socket.gethostname()}


class Result(BaseModel):
    comment: str  # any string to describe this result
    label: str  # class for this result. For grouping, etc
    timestamp: datetime = datetime.now()  # when was experiment object created
    hostname: str = socket.gethostname()  # which machine


