import os
from distutils.dir_util import copy_tree
from pathlib import Path
from stat import S_IRGRP, S_IROTH, S_IRWXU, S_IXGRP, S_IXOTH

import click

from podder_task_base.task_initializer.builders import TaskNameBuilder


class Builder(object):
    CHMOD755 = S_IRWXU | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH

    def __init__(self, task_name: str, target_dir: str) -> None:
        this_dir = Path(__file__).resolve().parent
        self.templates_dir = str(this_dir.joinpath("templates").resolve())
        self.target_dir = target_dir
        self.task_name = task_name
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)

    def init_task(self) -> None:
        copy_tree(self.templates_dir, self.target_dir)

        for path in Path(self.target_dir + "/scripts").glob("*.sh"):
            path.chmod(self.CHMOD755)

        builders = [
            [TaskNameBuilder, 'task_name.ini'                      , self.task_name],
            [TaskNameBuilder, 'api/task_api.py'                    , self.task_name],
            [TaskNameBuilder, 'api/grpc_server.py'                 , self.task_name],
            [TaskNameBuilder, 'api/protos/pipeline_framework.proto', self.task_name],
        ]
        self._build(
            builders=builders)

    def _build(self, builders: list) -> None:
        for builder, file, option in builders:
            builder(self.templates_dir).execute(self.target_dir, file, option)
        click.secho("{} : Completed successfully!".format(file), fg='green')
