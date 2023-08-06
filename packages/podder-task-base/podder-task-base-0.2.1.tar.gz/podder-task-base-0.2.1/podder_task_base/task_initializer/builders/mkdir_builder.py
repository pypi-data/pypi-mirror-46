import os
from typing import Any

from podder_task_base.task_initializer.builders.base_builder import BaseBuilder


class MkdirBuilder(BaseBuilder):
    def execute(self, target_dir: str, file: str, option: Any) -> None:
        dst_path = os.path.join(target_dir, file)
        os.mkdir(dst_path)
        if option is not None:
            os.chmod(dst_path, option)
