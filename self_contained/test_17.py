from __future__ import absolute_import, print_function, unicode_literals
from argparse import FileType
from importlib.machinery import SourceFileLoader
import os
import re
import fnmatch
import core
def source_file_filter(file_list, file_type_list):
    """
    Prune the file list for a specific type.

    Note: file_type_list can either be a single enums.FileTypes enum or an
        iterable list of enums.FileTypes

    Args:
        file_list: list of core.SourceFile entries.
        file_type_list: enums.FileTypes to match.
    Returns:
        list of matching core.SourceFile entries.
    """

    result_list = []

    # If a single item was passed, use a simple loop
    if isinstance(file_type_list, FileTypes):
        for item in file_list:
            if item.type is file_type_list:
                result_list.append(item)
    else:
        # A list was passed, so test against the list
        for item in file_list:
            if item.type in file_type_list:
                result_list.append(item)
    return result_list



def test_source_file_filter():
    """
    Check the corretness of source_file_filter
    """
        