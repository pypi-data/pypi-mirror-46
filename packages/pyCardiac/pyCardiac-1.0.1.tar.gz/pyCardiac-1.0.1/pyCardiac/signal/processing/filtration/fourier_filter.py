import numpy as np
from scipy.fftpack import rfft, irfft, rfftfreq
from ....routines import rescale


def fourier_filter(data: np.ndarray, fs: float,
                   lp_freq: float = None, hp_freq: float = None, bs_freqs: list = [],
                   trans_width: float = 1, band_width: float = 1) -> np.ndarray:
    
    """
    Fourer filter along last axis of ``data`` with lowpass, highpass and bandstop options.
    
    Parameters
    ----------
    ``data`` : np.ndarray
    ``fs``: float
        sampling frequency
    ``lp_freq``: float, optional
        lowpass frequency (default is None)
    ``hp_freq``: float, optional
        highpass frequency (default is None)
    ``bs_freqs``: list, optional
        bandstop frequencies (default is [])
    ``trans_width``: float, optional
        width of the transition region between bands (default is 1)
        in frequency units
    ``band_width``: float, optional
        width of the band to remove (default is 1)
        in frequency units
        
    Returns
    -------
    np.ndarray
        filtered ``data``
    """
    
    T = data.shape[-1]
    d = 1. / fs
    freq = rfftfreq(T, d)
    f_data = rfft(data, axis=-1)
    
    freq_resp = create_freq_resp(freq, lp_freq,
                                 hp_freq, bs_freqs,
                                 trans_width, band_width)
    
    f_data = np.apply_along_axis(lambda x: x * freq_resp, -1, f_data)
    data_filtered = irfft(f_data)
    
    return data_filtered


def create_freq_resp(freq: np.ndarray, lp_freq: float,
                     hp_freq: float, bs_freqs: list,
                     trans_width: float, band_width: float) -> np.ndarray:
    """Calculates frequency responce for given ``freq``
    
    Parameters
    ----------
    ``freq``: np.ndarray, shape=(N)
        frequency array
    ``lp_freq``: float
        lowpass frequency
    ``hp_freq``: float
        highpass frequency
    ``bs_freqs``: list
        bandstop frequencies
    ``trans_width``: float
        width of the transition region between bands
    ``band_width``: float
        width of the band to remove
        
    Returns
    --------
    np.ndarray, shape=(N)
        frequency responce array in range form 0 to 1
    """
    
    freq_resp = np.ones_like(freq)
    
    if lp_freq is not None:
        freq_resp *= FR_lowpass(freq, lp_freq, trans_width)
    
    if hp_freq is not None:
        freq_resp *= FR_highpass(freq, hp_freq, trans_width)
    
    for bs_freq in bs_freqs:
        freq_resp *= FR_bandstop(freq, bs_freq, trans_width, band_width)
        
    return freq_resp
    
    
def FR_lowpass(freq: np.ndarray, lp_freq: float,
               trans_width: float) -> np.ndarray:
    """Frequency responce for lowpass filter
    
    Parameters
    ----------
    ``freq``: np.ndarray
        frequency array
    ``lp_freq``: float
        lowpass frequency
    ``trans_width``: float
        width of the transition region between bands
        
    Returns
    -------
    np.ndarray
        with values in [0, 1]
    """
    
    sigma = trans_width / 6.
    return 1 / (1 + np.exp((freq - lp_freq) / sigma))


def FR_highpass(freq: np.ndarray, hp_freq: float,
                trans_width: float) -> np.ndarray:
    """Frequency responce for highpass filter
    
    Parameters
    ----------
    ``freq``: np.ndarray
        frequency array
    ``hp_freq``: float
        highpass frequency
    ``trans_width``: float
        width of the transition region between bands
        
    Returns
    -------
    np.ndarray
        with values in [0, 1]
    """
        
    sigma = trans_width / 6.
    return 1 / (1 + np.exp((hp_freq - freq) / sigma))


def FR_bandstop(freq: np.ndarray, bs_freq: float,
                trans_width: float, band_width: float) -> np.ndarray:
    """Frequency responce for bandstop filter
    
    Parameters
    ----------
    ``freq``: np.ndarray
        frequency array
    ``bs_freq``: float
        bandstop frequency
    ``trans_width``: float
        width of the transition region between bands
        
    Returns
    -------
    np.ndarray
        with values in [0, 1]
    """
        
    left = FR_lowpass(freq, bs_freq - band_width / 2., trans_width)
    right = FR_highpass(freq, bs_freq + band_width / 2., trans_width)
    return rescale(left + right)