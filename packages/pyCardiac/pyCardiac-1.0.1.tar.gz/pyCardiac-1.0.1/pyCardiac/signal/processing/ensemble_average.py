import numpy as np


def ensemble_average(time: np.ndarray, signal: np.ndarray, cycle_length: float) -> np.ndarray:
    """Ensemble average of ``signal``.
    
    Parameters
    ``time`` : np.ndarray, shape=(T)
    ``signal``: np.ndarray, shape=(T)
    ``cycle_length`` : int
        averaging interval
        
    Returns
    -------
    np.ndarray, shape=(``cycle_length``)
    
    Example
    -------
    >>> time = np.linspace(0, 100, 1000)
    >>> cycle_length = 15.
    >>> signal = np.sin(time / (cycle_length / (2 * np.pi)))
    >>> noise = 0.2 * np.sin(time / 0.42)
    >>> signal_noisy = signal + noise
    >>> plt.plot(time, signal_noisy)
    >>> plt.show()

    >>> time_space, signal_averaged = ensemble_average(time, signal_noisy, cycle_length)
    >>> plt.plot(time_space, signal_averaged)
    >>> plt.show()
    """
    
    time, signal = map(np.array, (time, signal))
        
    L = len(signal)
    if L != len(time):
        msg = "time and signal must be the same length but {0} and {1} are given".format(len(time), len(signal))
        raise Exception(msg)

    time_ptp = time.ptp()
    n = int(time_ptp / cycle_length)     # number of whole cycles
    m = int(L * cycle_length / time_ptp) # number of points in cycle
    
    signal_cut = signal[: (n * m)]
    
    L_tail = L - (n * m)
    signal_tail = np.zeros((m))
    signal_tail[:L_tail] += signal[-L_tail :]
    
    signal_tailed = np.hstack((signal_cut, signal_tail))
    signal_tailed_reshaped = signal_tailed.reshape((n + 1, m))
    
    signal_average = np.sum(signal_tailed_reshaped, axis = 0)
    signal_average[:L_tail] /= (n + 1)
    signal_average[L_tail:] /= n
    time_space = time[: m] - time[0]
    
    return time_space, signal_average
