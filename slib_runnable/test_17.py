"""
Goal: To search the given text in the data of type dict
"""

from collections import OrderedDict
import re



def get_pattern(pattern, strip=True):
    """
    This method converts the given string to regex pattern
    """
    if type(pattern) == re.Pattern:
        return pattern

    if strip and type(pattern) == str:
        pattern = pattern.strip()

    return re.compile(pattern)



def test_get_pattern():
    """Check the correctness of get_pattern
    """
    assert get_pattern('1.cpp',) == re.compile('1.cpp')
    assert get_pattern('4.cpp') == re.compile('4.cpp')
    assert get_pattern('9.h') == re.compile('9.h')