import random
import numpy as np
import pandas as pd

# Load the dataset
dataset = pd.read_csv('../data/census.csv')

def cluster_sampling(dataset, number_of_groups):
    interval = len(dataset) / number_of_groups

    groups = []
    group_id = 0
    count = 0
    for _ in dataset.iterrows():
        groups.append(group_id)
        count += 1
        if count > interval:
            count = 0
            group_id += 1

    dataset['group'] = groups
    random.seed(1)
    # selected_group = random.randint(0, number_of_groups)
    selected_group = random.randint(0, number_of_groups - 1)  # Updated 16/10/2023
    return dataset[dataset['group'] == selected_group]

df_cluster_sampling = cluster_sampling(dataset, 325)
print(df_cluster_sampling.shape, df_cluster_sampling['group'].value_counts())