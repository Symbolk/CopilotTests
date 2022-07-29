import subprocess
import collections
import glob
import inspect
import os
import random
import re
import shutil
import tempfile
import time
from contextlib import contextmanager
import sys
import psutil
import requests
from pathlib import Path
import socket
import platform

def is_local(host):
    """
    Checks if the host is the localhost

    :param host: The hostname or ip
    :return: True if the host is the localhost
    """
    return host in ["127.0.0.1",
                    "localhost",
                    socket.gethostname(),
                    # just in case socket.gethostname() does not work  we also try the following:
                    platform.node(),
                    socket.gethostbyaddr(socket.gethostname())[0]
                    ]


def test_is_local():
    """Check the correctness of is_local
    """
    assert is_local(' ') == False
    assert is_local('   ') == False
    assert is_local('127.0.0.1')   == True
    assert is_local('localhost')   == True
    assert is_local(' localhost ') == True
    assert is_local(platform.node()) == True
    assert is_local(socket.gethostbyaddr(socket.gethostname())[0]) == True
    assert is_local(socket.gethostname()) == True
    