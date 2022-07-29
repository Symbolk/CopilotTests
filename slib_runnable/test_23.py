import random
import numpy as np

def gaussian(x):
        """
        Gaussian centered around 0.2 with a sigma of 0.1.
        """
        mu = 0.2
        sigma = 0.1
        return np.exp(-(x-mu)**2/sigma**2)

def test_gaussian():
    """Check the correctness of gaussian
    """
    assert gaussian(0) == np.exp(-(0-0.2)**2/0.1**2)
    assert gaussian(1) == np.exp(-(1-0.2)**2/0.1**2)
    assert gaussian(2) == np.exp(-(2-0.2)**2/0.1**2)
    assert gaussian(3) == np.exp(-(3-0.2)**2/0.1**2)
    assert gaussian(4) == np.exp(-(4-0.2)**2/0.1**2)