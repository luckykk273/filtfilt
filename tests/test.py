import pandas as pd
import os 


root = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(root, 'test_case.csv')
    
df = pd.read_csv(path, header=None)
data = df.iloc[:, 0].to_numpy()
print()