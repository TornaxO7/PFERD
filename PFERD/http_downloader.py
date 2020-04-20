"""Contains a simple HTTP downloader that can handle HTTP basic auth."""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

import requests
import requests.auth

from .new_organizer import Organizer
from .tmp_dir import TmpDir
from .utils import stream_to_path


class HttpDownloader():
    """A HTTP downloader that can handle HTTP basic auth."""

    def __init__(self, tmp_dir: TmpDir, organizer: Organizer, username: Optional[str], password: Optional[str]):
        """Create a new http downloader."""
        self._organizer = organizer
        self._tmp_dir = tmp_dir
        self._username = username
        self._password = password
        self._session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        if self._username and self._password:
            session.auth = requests.auth.HTTPBasicAuth(
                self._username, self._password
            )
        return session

    def download(self, url: str, target_path: Path, parameters: Dict[str, Any] = {}) -> None:
        """Download a given url to a given path, optionally with some get parameters."""
        response = self._session.get(url, params=parameters)

        if response.status_code == 200:
            tmp_file = self._tmp_dir.new_file()
            stream_to_path(response, tmp_file)
            self._organizer.accept_file(tmp_file, target_path)
        else:
            raise Exception(
                f"Could not download file, got response {response.status_code}"
            )