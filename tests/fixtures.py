import pytest
import pandas as pd
import os


@pytest.fixture
def filtfilt_params():
    root = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(root, 'test_case.csv')
    df = pd.read_csv(path, header=None)
    data = df.iloc[:, 0].to_numpy()
    params = [
        [0.5, 50, 5],
        [0.5, 50, 2],
        [0.2, 50, 3],
        [0.2, 50, 8],
    ]
    return data, params
