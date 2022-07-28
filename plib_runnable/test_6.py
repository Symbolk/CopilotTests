"""
Classes for spectral analysis.
"""

import datetime
from copy import copy
from math import floor
from random import randint
from distutils.version import LooseVersion

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colorbar import Colorbar
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter, IndexLocator, MaxNLocator
from numpy import ma
from scipy import ndimage

__all__ = ["Spectrogram", "LinearTimeSpectrogram"]


# 1080 because that usually is the maximum vertical pixel count on modern
# screens nowadays (2012).
DEFAULT_YRES = 1080

# This should not be necessary, as observations do not take more than a day
# but it is used for completeness' and extendibility's sake.
# XXX: Leap second?
SECONDS_PER_DAY = 86400

# Used for COPY_PROPERTIES
REFERENCE = 0
COPY = 1
DEEPCOPY = 2




def make_array(shape, dtype=np.dtype("float32")):
    """
    Function to create an array with shape and dtype.

    Parameters
    ----------
    shape : tuple
        shape of the array to create
    dtype : `numpy.dtype`
        data-type of the array to create
    """
    return np.zeros(shape, dtype=dtype)



def test_make_array():
    """Check the correctness of make_array
    """
    assert make_array((3,4)).shape == (3,4)
    assert make_array((3,4), dtype=np.dtype("float64")).dtype == np.dtype("float64")
    assert make_array((3,4), dtype=np.dtype("float64")).shape == (3,4)
    assert make_array((3,4), dtype=np.dtype("float64"))[0][0]== 0
    assert make_array((3,4), dtype=np.dtype("float64"))[-1][-1]== 0