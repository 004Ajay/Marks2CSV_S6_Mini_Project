# Finding zero col, deletes zero col, find and drop col with no values at all 

import pandas as pd

data = {
        'name': ['Alice', 'Bob', 'Charlie'],
        '1a': [25, 30, 35],
        '1b': [],
        '1c':[0,0,0]
       }

print(len(data['name']))

df = pd.DataFrame(data, index=pd.RangeIndex(start=1, stop=len(data['name'])+1, name='Roll No')) # change stop value to len(names) # dict to df
col_name = df.columns[(df == 0).all()] # finding the column with all 0 values
df2 = df.drop(col_name, axis=1) # delete the column with 0 values only
final_csv = df2.dropna(axis=1,how='all') # drop columns with no values at all
df.to_csv('example.csv', index=True) # Export df to CSV file     # return final_csv or return df.ro_csv....