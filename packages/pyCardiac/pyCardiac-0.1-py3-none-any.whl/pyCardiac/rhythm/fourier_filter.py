import numpy as np
from ..signal.processing.filtration import fourier_filter as fourier_filter_1d


def fourier_filter(data: np.ndarray, Fs: float, *args) -> np.ndarray:
    """FFT filter of ``data`` along last axis.
    
    Parameters
    ----------
    ``data`` : np.ndarray, shape=(X, Y, N)
    ``Fs`` : float
        sampling frequency
    ``*args``
        variable length argument list.
        of frequency ranges, could be:
            [n, m], where n < m: region to trim
            [n, m], where n >= m: region to delete        
        *args are being applied sequentialy
        
    Returns
    -------
    np.ndarray, shape=(X, Y, N)
        filtered ``data``
    """
    
    data_filtered = np.apply_along_axis(fourier_filter_1d, -1, data, Fs, *args)
    return data_filtered