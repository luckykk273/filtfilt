from filtfilt import filtfilt
from scipy import signal
import numpy as np
from .fixtures import filtfilt_params


def test_filtfilt(filtfilt_params):
    data, params = filtfilt_params

    for cutoff_freq, fs, order in params:
        print(cutoff_freq, fs, order)
        # first get b, a using scipy
        nyquist_freq = 0.5 * fs
        normalized_cutoff_freq = cutoff_freq / nyquist_freq
        b, a = signal.butter(order, normalized_cutoff_freq, btype='low', analog=False)

        # test the result of filtfilt
        res_scipy = signal.filtfilt(b, a, data)
        res_self = filtfilt(b, a, data)
        assert np.allclose(res_scipy, res_self)

