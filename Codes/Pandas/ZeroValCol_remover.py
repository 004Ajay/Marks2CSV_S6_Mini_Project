import pandas as pd

df = pd.read_csv("data.csv")
col_name = df.columns[(df == 0).all()] # finding the column with all 0 values
df = df.drop(col_name, axis=1) # delete the column with 0 values only
df.to_csv("data_updated.csv", index=False) # Write the DataFrame back to another CSV file