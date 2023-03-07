import time
import pandas as pd

start_time = time.time()

df = pd.read_csv("tes.csv")
col_name = df.columns[(df == 0).all()] # finding the column with all 0 values
df2 = df.drop(col_name, axis=1) # delete the column with 0 values only
empty_col_rem = df2.dropna(axis=1,how='all') # drop columns with no values at all
df2.to_csv("data_updated.csv", index=False) # Write the DataFrame back to another CSV file

end_time = time.time()

print(f'Time taken: {end_time-start_time}')