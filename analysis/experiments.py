#############
#############
############# Experiments
#############
#############


import pandas as pd
import numpy as np

## Data reader
data_path = '../data/clean_data_full.csv'
df = pd.read_csv(data_path)
print df.head(10)
print df.info()
## Models