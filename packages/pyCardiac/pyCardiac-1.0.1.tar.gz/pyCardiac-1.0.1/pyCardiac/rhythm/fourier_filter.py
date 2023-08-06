import numpy as np
from ..signal.processing.filtration import fourier_filter as fourier_filter_1d


def fourier_filter(data: np.ndarray, fs: float,
                   lp_freq: float = None, hp_freq: float = None, bs_freqs: list = [],
                   trans_width: float = 1, band_width: float = 1) -> np.ndarray:
    
    data_filtered = fourier_filter_1d(data, fs,
                                      lp_freq, hp_freq, bs_freqs,
                                      trans_width, band_width)
    return data_filtered

fourier_filter.__doc__ = fourier_filter_1d.__doc__
