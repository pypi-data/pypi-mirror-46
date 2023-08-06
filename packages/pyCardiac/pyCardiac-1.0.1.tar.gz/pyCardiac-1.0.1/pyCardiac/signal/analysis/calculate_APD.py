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

    if not (0 < percentage < 100):
        msg = "percentage must be in range (0, 100) but {} was given".format(percentage)
        raise Exception(msg)

    index = np.nonzero(signal_copy < signal_copy.min() + (1. - percentage / 100.) * signal_copy.ptp())
    index = index[0]
    spaces = time_copy[index[1:]] - time_copy[index[:-1]]
    if (len(spaces)):
        APD = np.nanmax(spaces)
    else:
        APD = np.NaN
    return APD
