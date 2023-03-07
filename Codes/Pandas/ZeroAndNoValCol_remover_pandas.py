import pandas as pd

df = pd.read_csv("tes.csv")
print(df)
col_name = df.columns[(df == 0).all()] # finding the column with all 0 values
df2 = df.drop(col_name, axis=1) # delete the column with 0 values only
empty_col_rem = df2.dropna(axis=1,how='all') # drop columns with no values at all
print(empty_col_rem)