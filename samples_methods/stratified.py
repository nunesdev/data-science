import random
import numpy as np
import pandas as pd

# Load the dataset
dataset = pd.read_csv('../data/census.csv')

from sklearn.model_selection import StratifiedShuffleSplit

def stratified_sampling(dataset, percentage):
    split = StratifiedShuffleSplit(test_size=percentage, random_state=1)
    # _ = 20% (training), y = 80% of records (test)
    for _, y in split.split(dataset, dataset['income']):
        df_y = dataset.iloc[y]
    return df_y

df_stratified_sample = stratified_sampling(dataset, 0.0030711587481956942)
print(df_stratified_sample.head())
