import numpy as np


def _linear_filter(b: np.ndarray, a: np.ndarray, x: np.ndarray, zi: np.ndarray):
    input_size = x.size  # x is an 1D array
    # in general, size a, size b, size zi and size zf are with the same size
    filter_order = max(b.size, a.size)
    zf = np.zeros((zi.size+1, ))
    zf[:zi.size] = zi
    y = np.zeros((input_size, ))

    for i in range(input_size):
        y[i] = b[0] * x[i] + zf[0]
        for j in range(1, filter_order):
            zf[j - 1] = b[j] * x[i] + zf[j] - a[j] * y[i]
    
    return y, zf[:-1]


def lfilter(b: np.ndarray, a: np.ndarray, x: np.ndarray, zi: np.ndarray):
    if b.ndim != 1:
        raise ValueError('b must be at least 1-D.')
    if a.ndim != 1:
        raise ValueError('a must be at least 1-D.')
    if len(a) < 2:
        raise ValueError('length of a should be greater than 2.')
    if zi is None:
        raise ValueError('zi cannot be None.')

    return _linear_filter(b, a, x, zi)


def _companion(a: np.ndarray):
    if a.ndim != 1:
        raise ValueError("Incorrect shape for `a`.  `a` must be "
                         "one-dimensional.")

    if a.size < 2:
        raise ValueError("The length of `a` must be at least 2.")

    if a[0] == 0:
        raise ValueError("The first coefficient in `a` must not be zero.")

    first_row = -a[1:] / (1.0 * a[0])
    n = a.size
    c = np.zeros((n - 1, n - 1), dtype=first_row.dtype)
    c[0] = first_row
    c[list(range(1, n - 1)), list(range(0, n - 2))] = 1
    return c


def lfilter_zi(b: np.ndarray, a: np.ndarray):
    if b.ndim != 1:
        raise ValueError("Numerator b must be 1-D.")
    if a.ndim != 1:
        raise ValueError("Denominator a must be 1-D.")

    while len(a) > 1 and a[0] == 0.0:
        a = a[1:]
    if a.size < 1:
        raise ValueError("There must be at least one nonzero `a` coefficient.")

    if a[0] != 1.0:
        # Normalize the coefficients so a[0] == 1.
        b = b / a[0]
        a = a / a[0]

    n = max(len(a), len(b))

    # Pad a or b with zeros so they are the same length.
    if len(a) < n:
        a = np.r_[a, np.zeros(n - len(a), dtype=a.dtype)]
    elif len(b) < n:
        b = np.r_[b, np.zeros(n - len(b), dtype=b.dtype)]

    IminusA = np.eye(n - 1, dtype=np.result_type(a, b)) - _companion(a).T
    B = b[1:] - a[1:] * b[0]
    # Solve zi = A*zi + B
    zi = np.linalg.solve(IminusA, B)

    return zi
