import random
import numpy as np
import pandas as pd

dataset = pd.read_csv('../data/census.csv')

def simple_random_sampling(dataset, samples):
    return dataset.sample(n=samples, random_state=1)

# Apply simple random sampling to the dataset
df_simple_random_sample = simple_random_sampling(dataset, 3)
print(df_simple_random_sample.shape)
