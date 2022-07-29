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

def is_powershell():
    """
    True if you run in powershell

    :return: True if you run in powershell
    """
    # psutil.Process(parent_pid).name() returns -
    # cmd.exe for CMD
    # powershell.exe for powershell
    # bash.exe for git bash
    return (psutil.Process(os.getppid()).name() == "powershell.exe")


def test_is_powershell():
    """Check the correctness of is_powershell
    """
    assert is_powershell()==False