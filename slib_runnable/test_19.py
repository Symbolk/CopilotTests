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


# noinspection PyPep8
def is_gitbash():
    """
    returns True if you run in a Windows gitbash

    :return: True if gitbash
    """
    try:
        exepath = os.environ['EXEPATH']
        return "Git" in exepath
    except:
        return False





def test_is_gitbash():
    """Check the correctness of is_gitbash
    """
    assert is_gitbash() == False