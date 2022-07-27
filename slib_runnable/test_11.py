#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module handles doxygen

Build and clean doxygen data

See Also:
    makeprojects.cleanme, makeprojects.buildme

@package makeprojects.doxygen
"""

# pylint: disable=consider-using-f-string
# pylint: disable=super-with-arguments

from __future__ import absolute_import, print_function, unicode_literals

import os

########################################




def match(filename):
    """
    Check if the filename is a type that this module supports

    Args:
        filename: Filename to match
    Returns:
        False if not a match, True if supported
    """

    base_name = os.path.basename(filename)
    base_name_lower = base_name.lower()
    return base_name_lower == 'doxyfile'


def test_match():
    """Check the correctness of match
    """
    assert match('doxyfile')
    assert not match('doxygen.conf')
    assert not match('doxygen.conf.dist')
    assert not match('doxygen.conf.dist.dist')
    assert not match('doxygen.conf.dist.dist.dist')
    assert match('DOXyFile')
    assert match('DOXyFILE')