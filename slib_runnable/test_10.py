# Copyright 2019 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import os

import re
from urllib.parse import urlparse


def _encode_endpoint_path(backup_endpoint):
        """base64 encode an backup path for cross mounting support"""
        return base64.b64encode(
            str.encode(urlparse(backup_endpoint).path)).decode()


def test__encode_endpoint_path():
    """Check the correctness of _encode_endpoint_path
    """
    assert _encode_endpoint_path('/backup/path') == 'L2JhY2t1cC9wYXRo'
    assert _encode_endpoint_path('/backup/path/') == 'L2JhY2t1cC9wYXRoLw=='
    assert _encode_endpoint_path('/backup/path/with/slash') == 'L2JhY2t1cC9wYXRoL3dpdGgvc2xhc2g='