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
from burger import string_to_bool, is_string, import_py_script

# pylint: disable=consider-using-f-string

########################################



def validate_string(value):
    """
    Verify a value is a string.

    Check if the value is a string, if so, return the value as is or None.

    Args:
        value: Value to check.

    Returns:
        Value is string or None.

    Raises:
        ValueError
    """

    if value is not None:
        # Convert to bool
        if not is_string(value):
            raise ValueError('"{}" must be a string.'.format(value))
    return value

########################################



def test_validate_string():
    """Check the correctness of validate_string
    """
    assert validate_string('test') == 'test'
    assert validate_string(None) == None
    assert validate_string(b'123') == b'123'