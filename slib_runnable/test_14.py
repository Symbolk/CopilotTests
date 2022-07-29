#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The util module contains subroutines used everywhere.

@package makeprojects.util
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import re
import fnmatch

# pylint: disable=consider-using-f-string

########################################


def regex_dict(item):
    """
    Convert *.cpp keys to regex keys

    Given a dict where the keys are all filenames with wildcards, convert only
    the keys into equivalent regexes and leave the values intact.

    Example:

    rules = {
        '*.cpp':
            {'a': 'arf', 'b': 'bark', 'c': 'coo'},
        '*.h':
            {'h': 'help'}
    }
    regex_keys = regex_dict(rules)

    Args:
        item: dict to convert
    Returns:
        dict with keys converted to regexes
    """

    output = {}
    for key in item:
        output[re.compile(fnmatch.translate(key)).match] = item[key]
    return output

def test_regex_dict():
    """Check the correctness of regex_dict
    """
    assert regex_dict({'*.cpp': {'a': 'arf', 'b': 'bark', 'c': 'coo'}}) == {re.compile(fnmatch.translate('*.cpp')).match: {'a': 'arf','b': 'bark','c': 'coo'}}
    assert regex_dict({'*.h': {'h': 'help'}}) == {re.compile(fnmatch.translate('*.h')).match: {'h': 'help'}}
    assert regex_dict({'*.cpp': {'a': 'arf', 'b': 'bark', 'c': 'coo'}, '*.h': {'h': 'help'}}) == {re.compile(fnmatch.translate('*.cpp')).match: {'a': 'arf','b': 'bark','c': 'coo'}, re.compile(fnmatch.translate('*.h')).match: {'h': 'help'}}