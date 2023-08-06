import numpy as np
from ...metrics import sd
from ...routines import scalar_multiplications


def autoscaling(signal_to_scale, signal_reference):
    """ Autoscaling technique implementation.
        Based on the method of least squares (link: https://en.wikipedia.org/wiki/Least_squares)
        Parameters
        ----------
        ``signal_to_scale`` : array-like object, shape=(X)
        signal we want to scale
        ``signal_reference`` : array-like object, shape=(X)
        target signal
        
        Returns
        -------
        numpy.ndarray, shape=(X)
            scaled signal
        float
            standart distance (error between two signals)
        
    """
    
    c = scalar_multiplications(signal_to_scale, signal_reference)
    
    if c[1] == 0 or c[1] * c[1] - c[4] * c[3] == 0:
        alpha = 0
        beta = 0
    else:
        beta = (c[0] * c[1] - c[2] * c[3])/(c[1] * c[1] - c[4] * c[3])
        alpha = (c[2] - beta * c[4])/ c[1]
    
    signal_scaled = signal_to_scale * alpha + beta
    variance = sd(signal_scaled, signal_reference)
    
    return signal_scaled, variance
