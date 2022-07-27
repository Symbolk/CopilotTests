# Copyright 2010 OpenStack Foundation
# Copyright 2013 NTT corp.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Implementation of an image service that uses Glance as the backend"""

import copy
import itertools
import random
import shutil
import sys
import textwrap
import time
from typing import (Any, Callable, Dict, Iterable, List,  # noqa: H301
                    NoReturn, Optional, Tuple)            # noqa: H301
import urllib
import urllib.parse




def _parse_image_ref(image_href: str) -> Tuple[str, str, bool]:
    """Parse an image href into composite parts.

    :param image_href: href of an image
    :returns: a tuple of the form (image_id, netloc, use_ssl)
    :raises ValueError:

    """
    url = urllib.parse.urlparse(image_href)
    netloc = url.netloc
    image_id = url.path.split('/')[-1]
    use_ssl = (url.scheme == 'https')
    return (image_id, netloc, use_ssl)




def test__parse_image_ref():
    """Check the correctness of _parse_image_ref
    """
    assert _parse_image_ref('http://example.com/image_id') == ('image_id', 'example.com', False)
    assert _parse_image_ref('https://example.com/image_id') == ('image_id', 'example.com', True)
    assert _parse_image_ref('https://example.com/image_id.tar.gz') == ('image_id.tar.gz', 'example.com', True)
    assert _parse_image_ref('https://example.com/image_id.tar.gz.gz') == ('image_id.tar.gz.gz', 'example.com', True)
    assert _parse_image_ref('https://example.com/image_id.tar.gz.gz.gz') == ('image_id.tar.gz.gz.gz', 'example.com', True)
    