"""Functions and classes for Persisting things"""
import pickle
from pathlib import Path, PurePath
from typing import List

from pydantic import BaseModel

from trolleybenchmark.core import Result


class Results(BaseModel):
    """Contains results. For easy persisting"""
    contents: List[Result]
    description: str = ""

    def save(self, path_or_obj):
        if isinstance(path_or_obj, (str, Path)):
            with open(path_or_obj, 'wb') as f:
                pickle.dump(self, f)
        else:
            #  assume its a file-like object
            pickle.dump(self, path_or_obj)

    @classmethod
    def load(cls, path_or_obj) -> "Results":
        if isinstance(path_or_obj, (str, Path)):
            with open(path_or_obj, 'rb') as f:
                return pickle.load(f)
        else:
            #  assume its a file-like object
            return pickle.load(path_or_obj)


def load_results_or_create(path) -> Results:
    try:
        return Results.parse_file(path)
    except FileNotFoundError:
        return Results(contents=[])
