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
from swh.model.hashutil import hash_to_hex
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

# Aliasing the page results returned by `get_pages` method from the lister.
ArchListerPage = List[Dict[str, Any]]



def parse_desc_file(
        path: Path,
        repo: str,
        base_url: str,
        dl_url_fmt: str,
    ) -> Dict[str, Any]:
        """Extract package information from a 'desc' file.
        There are subtle differences between parsing 'official' and 'arm' des files

        Args:
            path: A path to a 'desc' file on disk
            repo: The repo the package belongs to

        Returns:
            A dict of metadata

            Example::

                {'api_url': 'https://archlinux.org/packages/core/x86_64/dialog/json',
                 'arch': 'x86_64',
                 'base': 'dialog',
                 'builddate': '1650081535',
                 'csize': '203028',
                 'desc': 'A tool to display dialog boxes from shell scripts',
                 'filename': 'dialog-1:1.3_20220414-1-x86_64.pkg.tar.zst',
                 'isize': '483988',
                 'license': 'LGPL2.1',
                 'md5sum': '06407c0cb11c50d7bf83d600f2e8107c',
                 'name': 'dialog',
                 'packager': 'Evangelos Foutras <foutrelis@archlinux.org>',
                 'pgpsig': 'pgpsig content xxx',
                 'project_url': 'https://invisible-island.net/dialog/',
                 'provides': 'libdialog.so=15-64',
                 'repo': 'core',
                 'sha256sum': 'ef8c8971f591de7db0f455970ef5d81d5aced1ddf139f963f16f6730b1851fa7',
                 'url': 'https://archive.archlinux.org/packages/.all/dialog-1:1.3_20220414-1-x86_64.pkg.tar.zst',  # noqa: B950
                 'version': '1:1.3_20220414-1'}
        """
        rex = re.compile(r"^\%(?P<k>\w+)\%\n(?P<v>.*)\n$", re.M)
        with path.open("rb") as content:
            parsed = rex.findall(content.read().decode())
            data = {entry[0].lower(): entry[1] for entry in parsed}

            if "url" in data.keys():
                data["project_url"] = data["url"]

            assert data["name"]
            assert data["filename"]
            assert data["arch"]

            data["repo"] = repo
            data["url"] = urljoin(
                base_url,
                dl_url_fmt.format(
                    base_url=base_url,
                    pkgname=data["name"],
                    filename=data["filename"],
                    arch=data["arch"],
                    repo=repo,
                ),
            )

            assert data["md5sum"]
            assert data["sha256sum"]
            data["checksums"] = {
                "md5sum": hash_to_hex(data["md5sum"]),
                "sha256sum": hash_to_hex(data["sha256sum"]),
            }
        return data



def test_parse_desc_file():
    """Check the correctness of parse_desc_file
    """
    assert parse_desc_file(Path('/tmp/archlinux_archive'), \
        'core', 'https://archive.archlinux.org/packages/', \
            'https://archive.archlinux.org/packages/{repo}/{base}/{pkgname}/{filename}') \
                == {'api_url': 'https://archlinux.org/packages/core/x86_64/dialog/json', 'arch': 'x86_64', \
                    'base': 'dialog', 'builddate': '1650081535', \
                        'csize': '203028', 'desc': 'A tool to display dialog boxes from shell scripts', \
                            'filename': 'dialog-1:1.3_20220414-1-x86_64.pkg.tar.zst', 'isize': '483988', \
                                'license': 'LGPL2.1', 'md5sum': '06407c0cb11c50d7bf83d600f2e8107c', \
                                'name': 'dialog', 'packager': 'Evangelos Foutras'}