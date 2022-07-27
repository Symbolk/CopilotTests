import binascii
import math
import os
import uuid as _uu
from typing import List, Optional
def string_to_int(string: str, alphabet: List[str]) -> int:
    """
    Convert a string to a number, using the given alphabet.

    The input is assumed to have the most significant digit first.
    """
    number = 0
    alpha_len = len(alphabet)
    for char in string:
        number = number * alpha_len + alphabet.index(char)
    return number

def test_string_to_int():
    """
    Check the corretness of string_to_int
    """
    assert string_to_int("b", ["a", "b", "c"]) == 1


