import pandas as pd
import time

st = time.time()

data = {
        'name': ['Alice', 'Bob', 'Charlie'],
        '1a': [25, 30, 35],
        '1b': [],
        '1c':[0,0,0],
        '1d':[41,22,13]
       }

# Removing empty lists & lists with all entries as 0        

new_data = {k: v for k, v in data.items() if v and len(v)>0 and (not all(val==0 for val in v))}

n_data = pd.DataFrame(new_data, index=pd.RangeIndex(start=1, stop=len(data['name'])+1, name='Roll No')) # change stop value to len(names) # dict to df

n_data.to_csv('example2.csv', index=True)

print(time.time() - st)