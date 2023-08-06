import os
from typing import Any


class BaseBuilder(object):
    def __init__(self, templates_dir) -> None:
        self.templates_dir = templates_dir

    def execute(self, target_dir: str, file: str, option: Any) -> None:
        raise NotImplementedError
