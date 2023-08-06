import io
import os
import subprocess
import zipfile
from pathlib import Path
from urllib.parse import urlparse

import click
import requests
import pip._internal

from podder_task_base.exceptions import DownloadUrlNotFoundError


class PodderLibInstall(object):
    def __init__(self, download_url:str) -> None:
        self.download_url = download_url

    def execute(self) -> None:
        if self.download_url == "":
            click.secho("not found DOWNLOAD_URL.", fg='red')
            raise DownloadUrlNotFoundError

        file_path = self._download_from_s3(self.download_url)
        self._install_podder_lib(file_path)

    def _download_from_s3(self, url: str) -> str:
        click.echo("Downloading the podder_lib...")
        request = requests.get(url, stream=True)

        file_path = urlparse(url).path
        extract_path = Path.home().resolve().joinpath(Path(file_path).name)
        with extract_path.open("wb") as f:
            f.write(request.content)

        return str(extract_path)

    def _install_podder_lib(self, file_path: str) -> None:
        click.echo("Installing podder-lib (full package)...")
        pip._internal.main(['install', '-U', file_path])
