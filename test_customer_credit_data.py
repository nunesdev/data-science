import pandas as pd
from samples_methods.simple import simple_random_sampling
from samples_methods.cluster import cluster_sampling
from samples_methods.stratified import stratified_sampling
from samples_methods.systematic import systematic_sampling
from samples_methods.reservoir import reservoir_sampling

dataset = pd.read_csv("data/credit_data.csv")

df_cluster = cluster_sampling(dataset,2)
df_simple = simple_random_sampling(dataset,1000)

df_stratified = stratified_sampling(dataset,20,"c#default")
df_systematic = systematic_sampling(dataset,1000)
df_reservoir = reservoir_sampling(dataset,1000)


print(df_reservoir.head())