import numpy as np


def snr(signal_noisy, signal_clean = None):
    """ Signal-to-noise ratio (SNR) calculation.
            
        Parameters
        ----------
        ``signal_noisy`` : array-like object
            noisy signal
        ``signal_clean`` : array-like object
            clean signal, optional (default is None)
            
        Returns
        -------
        float
            SNR value
    """
    
    if signal_clean is None:
        m = signal_noisy.mean(0)
        sd = signal_noisy.std(axis = 0, ddof = 0)
        ratio = np.where(sd == 0, 0, m / sd)
    
    else:
        noise = signal_noisy - signal_clean
        rms_signal_clean = np.sqrt(np.mean(signal_clean**2))
        rms_noise = np.sqrt(np.mean(noise**2))
        ratio = 20 * np.log10(rms_signal_clean / rms_noise)

    return ratio
