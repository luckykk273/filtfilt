import numpy as np


def _odd_ext(x: np.ndarray, n: int):
    """
    Odd extension is a "180 degree rotation" at the endpoints of the original array.
    """
    if x.ndim != 1:
        raise ValueError('%dD array given to x.  x must be an 1D array.' % x.ndim)
    
    if n < 1:
        return x
    if n > x.shape[0] - 1:
        raise ValueError(("The extension length n (%d) is too big. " +
                         "It must not exceed x.shape[axis]-1, which is %d.")
                         % (n, x.shape[0] - 1))
    left_end = x[0:1]
    left_ext = x[n:0:-1]
    right_end = x[-1:]
    right_ext = x[-2:-(n+2):-1]
    ext = np.hstack((2 * left_end - left_ext, x, 2 * right_end - right_ext))
    return ext


def _even_ext(x: np.ndarray, n: int):
    """
    Even extension is a "mirror image" at the boundaries of the original array.
    """
    if x.ndim != 1:
        raise ValueError('%dD array given to x.  x must be an 1D array.' % x.ndim)
    
    if n < 1:
        return x
    if n > x.shape[0] - 1:
        raise ValueError(("The extension length n (%d) is too big. " +
                         "It must not exceed x.shape[axis]-1, which is %d.")
                         % (n, x.shape[0] - 1))
    left_ext = x[n:0:-1]
    right_ext = x[-2:-(n+2):-1]
    ext = np.hstack((left_ext, x, right_ext))
    return ext


def _const_ext(x: np.ndarray, n: int):
    """
    Constant extension continues with the same values as the endpoints of the array.
    """
    if x.ndim != 1:
        raise ValueError('%dD array given to x.  x must be an 1D array.' % x.ndim)
    
    if n < 1:
        return x
    left_end = x[0:1]
    ones = np.ones((n, ), dtype=x.dtype)
    left_ext = ones * left_end
    right_end = x[-1:]
    right_ext = ones * right_end
    ext = np.hstack((left_ext, x, right_ext))
    return ext


def validate_pad(padtype: str, padlen: int, x: np.ndarray, ntaps: int):
    """Helper to validate padding for filtfilt"""
    if x.ndim != 1:
        raise ValueError('%dD array given to x.  x must be an 1D array.' % x.ndim)

    if padtype not in ['even', 'odd', 'constant', None]:
        raise ValueError(("Unknown value '%s' given to padtype.  padtype "
                          "must be 'even', 'odd', 'constant', or None.") %
                         padtype)

    if padtype is None:
        padlen = 0

    if padlen is None:
        # Original padding; preserved for backwards compatibility.
        edge = ntaps * 3
    else:
        edge = padlen

    # x's 'axis' dimension must be bigger than edge.
    if x.shape[0] <= edge:
        raise ValueError("The length of the input vector x must be greater "
                         "than padlen, which is %d." % edge)

    if padtype is not None and edge > 0:
        # Make an extension of length `edge` at each
        # end of the input array.
        if padtype == 'even':
            ext = _even_ext(x, edge)
        elif padtype == 'odd':
            ext = _odd_ext(x, edge)
        else:
            ext = _const_ext(x, edge)
    else:
        ext = x
    return edge, ext