
import bisect
import calendar
import encodings
import logging
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import timedelta
from distutils import spawn
from subprocess import CalledProcessError

import psutil
from cached_property import cached_property


def unquote(name):
    """Remove quote from the given name."""
    assert isinstance(name, bytes)

    # This function just gives back the original text if it can decode it
    def unquoted_char(match):
        """For each ;000 return the corresponding byte."""
        if len(match.group()) != 4:
            return match.group
        try:
            return bytes([int(match.group()[1:])])
        except ValueError:
            return match.group

    # Remove quote using regex
    return re.sub(b";[0-9]{3}", unquoted_char, name, re.S)



def test_unquote():
    """Check the correctness of unquote
    """
    assert unquote(b"Hello") == b"Hello"
    assert unquote(b"Hello;000") == b'Hello\x00'
    assert unquote(b"Hello;001") == b'Hello\x01'
    assert unquote(b"Hello;002") == b'Hello\x02'
    assert unquote(b"Hello;003") == b'Hello\x03'
    assert unquote(b"Hello;004") == b'Hello\x04'