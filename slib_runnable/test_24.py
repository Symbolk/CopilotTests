# Copyright (C) 2022  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information
import datetime
import logging
from pathlib import Path
import re
import tarfile
from typing import Any, Dict, Iterator, List, Optional
from urllib.parse import unquote, urljoin

from bs4 import BeautifulSoup
import requests



def get_repo_archive(url: str, destination_path: Path) -> Path:
    """
    Given an url and a destination path, retrieve and extract .tar.gz archive
    which contains 'desc' file for each package.
    Each .tar.gz archive corresponds to an Arch Linux repo ('core', 'extra', 'community').

    Args:
        url: url of the .tar.gz archive to download
        destination_path: the path on disk where to extract archive

    Returns:
        a directory Path where the archive has been extracted to.
    """
    res = requests.get(url)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_bytes(res.content)

    extract_to = Path(str(destination_path).split(".tar.gz")[0])
    tar = tarfile.open(destination_path)
    tar.extractall(path=extract_to)
    tar.close()

    return extract_to

def test_get_repo_archive():
    """Check the correctness of get_repo_archive
    """
    assert get_repo_archive('https://dl.bintray.com/sherpa/sherpa-repo/sherpa-repo-core-2020-01-01.tar.gz', Path('/tmp/sherpa-repo-core-2020-01-01.tar.gz')) == Path('/tmp/sherpa-repo-core-2020-01-01')