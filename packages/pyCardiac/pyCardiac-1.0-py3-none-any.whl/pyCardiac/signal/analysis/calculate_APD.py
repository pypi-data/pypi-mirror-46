import numpy as np


def calculate_APD(time, signal, percentage = 80.):
    """ Calculate Action Potential Duration for ``percentage`` level repolarization of the ``signal``.
    
    Parameters
    ----------
    ``time`` : np.ndarray, shape=(T)
    ``signal`` : np.ndarray, shape=(T)
    ``percentage`` : float, optional
        level of signal to calculate duration (default is 80)
        
    Returns
    -------
    float or np.NaN
        APD in time units of ``time``
    """
    
    time_copy, signal_copy = map(np.array, (time, signal))

    assert(0 < percentage < 100)
    assert(len(time_copy.shape) == len(signal_copy.shape))
    assert(time_copy.shape == signal_copy.shape)

    index = np.nonzero(signal_copy < signal_copy.min() + (1. - percentage / 100.) * signal_copy.ptp())
    index = index[0]
    spaces = time_copy[index[1:]] - time_copy[index[:-1]]
    if (len(spaces)):
        APD = np.nanmax(spaces)
    else:
        APD = np.NaN
    return APD
