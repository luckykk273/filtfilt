import numpy as np
from .filt_utils import lfilter, lfilter_zi
from .array_utils import validate_pad


def filtfilt(b: np.ndarray, a: np.ndarray, x: np.ndarray, padtype='odd', padlen=None):
    """
    'pad' method supported only.
    """
    edge, ext = validate_pad(padtype, padlen, x, ntaps=max(len(a), len(b)))

    # Get the steady state of the filter's step response.
    zi = lfilter_zi(b, a)

    # Reshape zi and create x0 so that zi*x0 broadcasts
    # to the correct value for the 'zi' keyword argument
    # to lfilter.
    zi_shape = [1] * x.ndim
    zi_shape[0] = zi.size
    zi = np.reshape(zi, zi_shape)
    x0 = ext[:1]

    # Forward filter.
    (y, _) = lfilter(b, a, ext, zi * x0)

    # Backward filter.
    # Create y0 so zi*y0 broadcasts appropriately.
    y0 = y[-1:]
    (y, _) = lfilter(b, a, y[::-1], zi * y0)

    # Reverse y.
    y = y[::-1]

    if edge > 0:
        # Slice the actual signal from the extended signal.
        y = y[edge:-edge]

    return y
