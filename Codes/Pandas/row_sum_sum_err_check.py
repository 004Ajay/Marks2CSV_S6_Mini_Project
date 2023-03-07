import pandas as pd

# create a sample DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 55, 6], 'C': [7, 8, 9]})

# create a new column "row_sum" with the sum of each row
df = df.assign(sum=df.sum(axis=1))

# add a new column "error" with "Error" if row_sum is greater than 50
df = df.assign(Sum_more_than_50=df.apply(lambda x: 'Error' if x['sum'] > 50 else '', axis=1))

print(df)

df.to_csv("my.csv", index=False)