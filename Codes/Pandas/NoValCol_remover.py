import pandas as pd

df = pd.read_csv("tes.csv")
empty_col_rem = df.dropna(axis=1,how='all') # drop columns with no values at all
print(empty_col_rem)