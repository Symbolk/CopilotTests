import platform
import sys
import os
from pathlib import Path

from collections import OrderedDict
import pip
import psutil

import re
import multiprocessing





def os_is_mac():
    """
    Checks if the os is macOS

    :return: True is macOS
    :rtype: bool
    """
    return platform.system() == "Darwin"






def test_os_is_mac():
    """Check the correctness of os_is_mac
    """
    assert os_is_mac() == (platform.system()=="Darwin")