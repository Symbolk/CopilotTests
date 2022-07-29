#  -------------------------------------------------------------------
#  
#  Copyright (C) 2006-2022, Andrew W. Steiner
#  
#  This file is part of O2sclpy.
#  
#  O2sclpy is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  O2sclpy is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with O2sclpy. If not, see <http://www.gnu.org/licenses/>.
#  
#  -------------------------------------------------------------------
#
import sys

# For os.getenv()
import os

# For numpy.bytes_
import numpy

# To test between Linux/OSX using system()
import platform

# For CDLL loading
import ctypes
from ctypes.util import find_library


def force_string(obj):
    """
    This function returns the bytes object corresponding to ``obj``
    in case it is a string using UTF-8. 
    """
    if isinstance(obj,numpy.bytes_)==True or isinstance(obj,bytes)==True:
        return obj.decode('utf-8')
    return obj




def test_force_string():
    """Check the correctness of force_string
    """
    assert force_string(b'abc') == 'abc'
    assert force_string('abc') == 'abc'
    assert force_string(b'abcd') == 'abcd'
    assert force_string(numpy.bytes_(b'abc')) == 'abc'
    assert force_string(numpy.bytes_('abcd')) == 'abcd'
    