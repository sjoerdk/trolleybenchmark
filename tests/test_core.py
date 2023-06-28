from trolleybenchmark.core import Experiment, Result


class TestResult(Result):
    some_value: str


class TestExperiment(Experiment):

    def __init__(self, arg1):
        super().__init__(label="", comment="")
        self.arg1 = arg1

    def run(self):
        return TestResult(some_value=self.arg1, **self.get_default_result_args())


def test_experiment():
    """Run a basic experiment. Nothing should crash"""

    simple = TestExperiment(arg1="arg")
    result = simple.run()
    assert result

