import random
import numpy as np
import pandas as pd

def systematic_sampling(dataset, samples):
    interval = len(dataset) // samples
    random.seed(1)
    start = random.randint(0, interval)
    indices = np.arange(start, len(dataset), step=interval)
    systematic_sample = dataset.iloc[indices]
    return systematic_sample

# Apply systematic sampling to the dataset
#df_systematic_sample = systematic_sampling(dataset, 100)
#print(df_systematic_sample.shape)
