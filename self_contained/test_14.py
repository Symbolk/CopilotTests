import logging
import os
import re
import signal
import sys
import threading
import traceback
import warnings
from argparse import ArgumentParser
from collections import OrderedDict
from configparser import RawConfigParser, SectionProxy
from datetime import datetime, timezone
from hashlib import md5
from tempfile import NamedTemporaryFile
from time import time
from unittest import TestCase
def _dictsum(dicts):
    """
    Combine values of the dictionaries supplied by iterable dicts.

    >>> _dictsum([{'a': 1, 'b': 2}, {'a': 5, 'b': 0}])
    {'a': 6, 'b': 2}
    """
    it = iter(dicts)
    first = next(it).copy()
    for d in it:
        for k, v in d.items():
            first[k] += v
    return first


def test__dictsum():
    """
    Check the corretness of _dictsum
    """
    assert  _dictsum([{'a': 1, 'b': 2}, {'a': 5, 'b': 0}]) == {'a': 6, 'b': 2}
    assert _dictsum([{'a': 1, 'b': 2}, {'a': 5, 'b': 0}]) == {'a': 6, 'b': 2}
    assert _dictsum([{'a': 1, 'b': 2}, {'a': 5, 'b': 0}]) == {'a': 6, 'b': 2}
    assert _dictsum([{'a': 1, 'b': 2}, {'a': 5, 'b': 0}]) == {'a': 6, 'b': 2}