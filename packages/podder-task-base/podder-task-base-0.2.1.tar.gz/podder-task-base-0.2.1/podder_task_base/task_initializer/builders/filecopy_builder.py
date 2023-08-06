import os
import shutil
from typing import Any

from podder_task_base.task_initializer.builders.base_builder import BaseBuilder


class FilecopyBuilder(BaseBuilder):
    def execute(self, target_dir: str, file: str, option: Any) -> None:
        src_path = os.path.join(self.templates_dir, file)
        dst_path = os.path.join(target_dir, file)
        shutil.copyfile(src_path, dst_path)
        if option is not None:
            os.chmod(dst_path, option)
