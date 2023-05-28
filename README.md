# filtfilt
A zero-phase digital filtering implementation in Python.

# Usage
If you only want to run the function `filtfilt()` without tests:
```
poetry install --no-dev
```
If you also want to run the tests:
```
poetry install
```

After installing all necessary dependencies, run:
```
pytest
```

Or read your own data, get `b` and `a`, and then pass into `filtfilt()`.

# Note
For simplification, 
1. 1D array support only.
2. Padding method support only.


# Reference
[linear filter](https://github.com/KBaur/FiltFilt)