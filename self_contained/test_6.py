import binascii
import math
import os
import uuid as _uu
from typing import List, Optional
def int_to_string(number: int, alphabet: List[str], padding: Optional[int] = None) -> str:
    """
    Convert a number to a string, using the given alphabet.

    The output has the most significant digit first.
    """
    output = ""
    alpha_len = len(alphabet)
    while number:
        number, digit = divmod(number, alpha_len)
        output += alphabet[digit]
    if padding:
        remainder = max(padding - len(output), 0)
        output = output + alphabet[0] * remainder
    return output[::-1]


def test_int_to_string():
    """
    Check the corretness of int_to_string
    """
    assert int_to_string(1, ["a", "b", "c"]) == "b"
    assert int_to_string(1, ["a", "b", "c"], padding=3) == "aab"
    assert int_to_string(1, ["a", "b", "c"], padding=4) == "aaab"
    assert int_to_string(1, ["a", "b", "c"], padding=5) == "aaaab"
    assert int_to_string(1, ["a", "b", "c"], padding=6) == "aaaaab"
    assert int_to_string(1, ["a", "b", "c"], padding=7) == "aaaaaab"
    assert int_to_string(1, ["a", "b", "c"], padding=8) == "aaaaaaab"
