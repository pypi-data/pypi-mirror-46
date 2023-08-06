import numpy as np


def calculate_alternance(time: np.ndarray, signal: np.ndarray, percentage: float = 80., APD_min: float = 10.) -> float:
    """Calculate alternance of Action Potential for ``percentage`` level repolarization of the ``signal``.
    
    Parameters
    ----------
    ``time`` : np.ndarray, shape=(T)
    ``signal`` : np.ndarray, shape=(T)
    ``percentage`` : float, optional
        level of signal to calculate duration (default is 80)
    ``APD_min`` : float, optional
        min action potential duration expected (default is 10)
        
    Returns
    -------
    float or np.NaN
        alternance in time units of ``time``
    """

    time_copy, signal_copy = map(np.array, (time, signal))

    assert(0 < percentage < 100)
    assert(len(time_copy.shape) == len(signal_copy.shape))
    assert(time_copy.shape == signal_copy.shape)

    index = np.nonzero(signal_copy < signal_copy.min() + (1. - percentage / 100.) * signal_copy.ptp())
    index = index[0]
    spaces = time_copy[index[1:]] - time_copy[index[:-1]]

    try:
        max_first = np.argmax(spaces > APD_min)
        max_second = max_first + 1 + np.argmax(spaces[max_first + 1: ] > APD_min)
        alternance_value = spaces[max_first] - spaces[max_second]
    except:
        alternance_value = np.NaN
    return alternance_value
