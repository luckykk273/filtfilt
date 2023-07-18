# filtfilt
A zero-phase digital filtering implementation in Python.  
**This repository is just to re-implement the `scipy.signal.filtfilt()` in pure Python.**

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
[scipy.signal.filtfilt](https://github.com/scipy/scipy/blob/909baa6b21a884afa8f8e1f8f3226fa9e55bc2ad/scipy/signal/_signaltools.py#L4000)  
[linear filter](https://github.com/KBaur/FiltFilt)
