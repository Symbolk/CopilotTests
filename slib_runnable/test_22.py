"""
A convenient method to execute shell commands and return their output. Note:
that this method requires that the command be completely execute before the
output is returned. FOr many activities in cloudmesh this is sufficient.

"""
import errno
import glob
import os
import platform as os_platform
import requests
import shlex
import shutil
import subprocess
import sys
import textwrap
import zipfile
from pathlib import Path
from pipes import quote
from sys import platform
from tqdm import tqdm

import psutil


# from functools import wraps
# def timer(func):
#    @wraps(func)
#    def wrapper(*args,**kwargs):
#        print(f"{func.__name__!r} begins")
#        start_time = time.time()
#        result = func(*args,**kwargs)
#        print(f"{func.__name__!r} ends in {time.time()-start_time}  secs")
#        return result
#    return wrapper

# def NotImplementedInWindows(f):
#    def new_f(*args):
#        if sys.platform == "win32":
#            Console.error("The method {f.__name__} is not implemented in Windows,"
#                        " please implement, and/or submit an issue.")
#            sys.exit()
#        f(args)
#    return new_f

def windows_not_supported(f):
    def wrapper(*args, **kwargs):
        host = get_platform()
        if host == "windows":
            Console.error("Not supported on windows")
            return ""
        else:
            return f(*args, **kwargs)

    return wrapper

def NotImplementedInWindows():
    if sys.platform == "win32":
        Console.error(f"The method {__name__} is not implemented in Windows.")
        sys.exit()


def oneline(script, seperator=" && "):
    """
    converts a script to one line command.
    THis is useful to run a single ssh command and pass a one line script.

    :param script:
    :return:
    """
    return seperator.join(textwrap.dedent(script).strip().splitlines())




def test_oneline():
    """Check the correctness of oneline
    """
    assert oneline("hello") == "hello"
    assert oneline("hello\nworld") == "hello && world"
    assert oneline("hello\nworld\n") == "hello && world"
    assert oneline("hello\nworld\n", ";") == "hello;world"
    assert oneline("hello\nworld\n", "&&") == "hello&&world"
    assert oneline("hello\nworld\n", "||") == "hello||world"
    assert oneline("hello\nworld\n", ";|") == "hello;|world"