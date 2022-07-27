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

def remove_ending_os_sep(input_list):
    """
    Iterate over a string list and remove trailing os seperator characters.

    Each string is tested if its length is greater than one and if the last
    character is the pathname seperator. If so, the pathname seperator character
    is removed.

    Args:
        input_list: list of strings

    Returns:
        Processed list of strings

    Raises:
        TypeError
    """

    # Input could be None, so test for that case
    if input_list is None:
        return []

    return [item[:-1] if len(item) >= 2 and item.endswith(os.sep)
            else item for item in input_list]

########################################



def test_remove_ending_os_sep():
    """Check the correctness of remove_ending_os_sep
    """
    assert remove_ending_os_sep(['a', 'b', 'c']) == ['a', 'b', 'c']
    assert remove_ending_os_sep(['a', 'b', 'c' + os.sep]) == ['a', 'b', 'c']
    assert remove_ending_os_sep(['a', 'b', 'c' + os.sep * 2]) == ['a', 'b', 'c' + os.sep]
    assert remove_ending_os_sep(['a', 'b', 'c' + os.sep * 3]) == ['a', 'b', 'c' + os.sep * 2]