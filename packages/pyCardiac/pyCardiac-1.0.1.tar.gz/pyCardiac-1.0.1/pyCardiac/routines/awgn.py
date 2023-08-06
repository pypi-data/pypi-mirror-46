import numpy as np

def awgn(signal: np.ndarray, snr_db: float) -> np.ndarray:
    """Adding Additive Gaussian White Noise (AWGN) to a ``signal``.
    
    Parameters
    ----------
    ``signal`` : np.ndarray
        Array to add AWGN    
    ``snr_db`` : float
        given SNR (specified in dB)
        
    Returns
    -------
    np.ndarray
        signal with AWGN
    """
    
    signal = np.asanyarray(signal)
    
    snr_linear = 10**(snr_db / 10)
    power = np.sum(signal * signal) / (signal.size)
    sigma = np.sqrt(power / snr_linear)
    noise = sigma * np.random.normal(0, 1, signal.size)
    signal_noisy = signal + noise
    return signal_noisy
