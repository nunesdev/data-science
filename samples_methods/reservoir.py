import random
import numpy as np
import pandas as pd

# Create data
dataset = pd.read_csv('../data/census.csv')

def reservoir_sampling(dataset, samples):
    stream = []
    for i in range(len(dataset)):
        stream.append(i)

    i = 0
    size = len(dataset)

    reservoir = [0] * samples
    for i in range(samples):
        reservoir[i] = stream[i]

    while i < size:
        j = random.randrange(i + 1)
        if j < samples:
            reservoir[j] = stream[i]
        i += 1

    return dataset.iloc[reservoir]

# Apply reservoir sampling to the dataset
df_reservoir_sampling = reservoir_sampling(dataset, 100)
print(df_reservoir_sampling.shape)
