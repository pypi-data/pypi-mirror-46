import numpy as np
from scipy.fftpack import rfft, irfft, fftfreq


def fourier_filter(data: np.ndarray, Fs: float, *args) -> np.ndarray:
    """FFT filter of data.
    
    Parameters
    ----------
    ``data`` : np.ndarray, shape=(N)
        signal to filter
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
    np.ndarray, shape=(N)
        filtered data
    """
    
    n = len(data)
    signal = data.copy()
    time   = 1. * np.arange(0, n) / Fs
    d = 1. / Fs
    freq = fftfreq(n, d)
    f_signal = rfft(signal)
    cut_f_signal = f_signal.copy()
    
    mask = np.ones_like(freq, dtype = bool)
    
    for arg in args:
        
        assert(isinstance(arg, tuple) or isinstance(arg, list))
        assert(len(arg) == 2)
        
        first, second = arg
        
        if first < second: 
            low, up = first, second
            mask *= (freq >= low) * (freq <= up)  
        else:
            low, up = second, first
            mask *= (freq < low) + (freq > up)

    cut_f_signal[~mask] = 0     
    cut_signal = irfft(cut_f_signal)
    
    return cut_signal