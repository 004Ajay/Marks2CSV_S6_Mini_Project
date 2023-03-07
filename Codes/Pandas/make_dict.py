import pandas as pd
import time

st = time.time()

d_data = {
'Roll No': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63],
'Name': ['ABDUL JALEEL', 'ABHIJITH P R', 'ADARSH P R', 'AJAY T SHAJU', 'ALAIKA SAJI', 'ALAN ANTO', 'ALAN VARGHESE', 'ALDRIN IMMANUEL P S', 'ALEENA JAMES', 'ALEENA ROY', 'ANSU SUKU JOHN', 'ANTONY HAMLIN BEVEIRA', 'ARJUN P', 'ASHLY ELIZEBATH JOSEPH', 'ASIF T.S', 'ASWIN JEEV JOHNY', 'BASIL P BABU', 'BASIL SIBY', 'BEN BABY', 'BIJO THOMAS', 'CYRIL K SONY', 'DEEPTHA SHAJI', 'DEEPU SASI', 'DUA ASHRA', 'EFFRON RIFON', 'EMIL SAJ ABRAHAM', 'FELIX R', 'FREDI JACOB', 'GEO GEORGE', 'GEORGE JOYAL VINCENT', 'GILBERT GEORGE', 'GOURI S GOVIND', 'HARI KRISHNAN A', 'HASHIF V S', 'HRUDYA N NAIR', 'IMMANUEL BIJU', 'JAIDON GILL SHAJAN', 'JAYASANKAR SHYAM', 'JERRY PAUL', 'JISNOY JINSO', 'JOMAL P JOY', 'JOSEPH VARKICHEN', 'JUDIN AUGUSTIN', 'JUSTIN THOMAS JO', 'NAMITHA PRAMOD', 'NIKITH VARGHESE', 'NOYAL JOSEPH', 'PRIYAN V', 'RICHA ANN ABRAHAM', 'RUBEN JOHN VARGHESE', 'SAIRA SUSAN JOHN', 'SANDRA ANN THOMAS', 'SHORN VITTALIS', 'SIDHARTH U NAIR', 'STEPHEN C A', 'THOMSON THOMAS', 'THUSHAR THOMAS THAKADIPURATH', 'TOM J CHERUVIL', 'VARUN VIJAYAN', 'VISHNUPRASAD K G'],
'1a':   [1.0, 3.0, 'nan', 1.0, 3.0, 3.0, 0.0, 0.0, 2.0, 0.0, 'nan', 3.0, 0.0, 3.0, 1.0, 1.0, 0.0, 0.0, 2.0, 0.0, 3.0, 3.0, 2.0, 3.0, 3.0, 1.0, 0.0, 0.0, 0.0, 'nan', 1.0, 0.0, 2.0, 0.0, 1.0, 'nan', 'nan', 2.0, 3.0, 2.0, 1.0, 0.0, 0.0, 0.0, 2.0, 0.0, 'nan', 2.0, 3.0, 'nan', 3.0, 2.0, 1.0, 0.0, 3.0, 0.0, 2.0, 3.0, 1.0, 1.0],
'2a':   [0.0, 0.0, 'nan', 2.0, 2.0, 0.0, 2.0, 0.0, 0.0, 0.0, 'nan', 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 2.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'nan', 'nan', 2.0, 1.0, 2.0, 0.0, 0.0, 1.0, 2.0, 2.0, 0.0, 'nan', 1.0, 3.0, 'nan', 2.0, 1.0, 1.0, 'nan', 0.0, 3.0, 2.0, 1.0, 1.0, 0.0],
'3a':   [1.0, 3.0, 'nan', 2.0, 2.0, 2.0, 2.0, 0.0, 2.0, 2.0, 'nan', 3.0, 2.0, 3.0, 2.0, 1.0, 2.0, 0.0, 1.0, 2.0, 3.0, 0.0, 3.0, 2.0, 3.0, 0.0, 3.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 'nan', 'nan', 3.0, 3.0, 0.0, 2.0, 0.0, 2.0, 2.0, 3.0, 2.0, 2.0, 2.0, 1.0, 'nan', 1.0, 2.0, 2.0, 'nan', 0.0, 3.0, 2.0, 1.0, 'nan', 2.0],
'4a':   [0.0, 0.0, 'nan', 2.0, 1.0, 3.0, 0.0, 2.0, 3.0, 3.0, 'nan', 3.0, 0.0, 3.0, 2.0, 'nan', 3.0, 0.0, 3.0, 2.0, 3.0, 1.0, 3.0, 1.0, 2.0, 1.0, 2.0, 2.0, 0.0, 0.0, 3.0, 2.0, 0.0, 3.0, 3.0, 'nan', 1.0, 1.0, 3.0, 2.0, 1.0, 0.0, 3.0, 3.0, 3.0, 1.0, 2.0, 3.0, 3.0, 'nan', 3.0, 1.0, 1.0, 'nan', 1.0, 3.0, 1.0, 0.0, 'nan', 2.0],
'5a':   [2.0, 2.0, 'nan', 2.0, 2.0, 3.0, 1.0, 0.0, 2.0, 2.0, 'nan', 0.0, 2.0, 2.0, 2.0, 'nan', 0.0, 0.0, 0.0, 0.0, 2.0, 2.0, 2.0, 1.0, 2.0, 1.0, 1.0, 2.0, 0.0, 1.0, 3.0, 2.0, 1.0, 1.0, 0.0, 'nan', 1.0, 2.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 1.0, 0.0, 0.0, 2.0, 3.0, 'nan', 2.0, 2.0, 1.0, 'nan', 2.0, 3.0, 1.0, 0.0, 'nan', 0.0],
'6a':   [4.0, 7.0, 'nan', 0.0, 7.0, 7.0, 7.0, 0.0, 7.0, 7.0, 3.0, 0.0, 6.0, 6.0, 7.0, 'nan', 4.0, 0.0, 7.0, 5.0, 6.0, 7.0, 0.0, 7.0, 7.0, 7.0, 6.0, 6.0, 6.0, 0.0, 7.0, 7.0, 2.0, 7.0, 7.0, 7.0, 3.0, 7.0, 7.0, 6.0, 6.0, 7.0, 6.0, 7.0, 7.0, 7.0, 6.0, 0.0, 7.0, 7.0, 7.0, 0.0, 6.0, 'nan', 6.0, 'nan', 0.0, 7.0, 1.0, 7.0],
'7a':   [0.0, 6.0, 'nan', 7.0, 0.0, 7.0, 0.0, 0.0, 0.0, 7.0, 3.0, 2.0, 0.0, 0.0, 6.0, 'nan', 4.0, 7.0, 6.0, 5.0, 0.0, 7.0, 7.0, 7.0, 7.0, 7.0, 6.0, 6.0, 5.0, 2.0, 7.0, 4.0, 0.0, 3.0, 6.0, 6.0, 3.0, 0.0, 7.0, 0.0, 0.0, 7.0, 6.0, 0.0, 0.0, 0.0, 0.0, 4.0, 7.0, 6.0, 7.0, 0.0, 0.0, 'nan', 0.0, 3.0, 4.0, 7.0, 'nan', 2.0],
'8a':   [4.0, 3.0, 'nan', 7.0, 7.0, 0.0, 4.0, 3.0, 7.0, 4.0, 'nan', 7.0, 0.0, 5.0, 4.0, 1.0, 0.0, 4.0, 5.0, 1.0, 6.0, 0.0, 7.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 6.0, 4.0, 2.0, 0.0, 0.0, 3.0, 2.0, 7.0, 2.0, 6.0, 6.0, 0.0, 0.0, 7.0, 7.0, 7.0, 6.0, 4.0, 0.0, 0.0, 0.0, 6.0, 6.0, 'nan', 6.0, 7.0, 4.0, 0.0, 2.0, 6.0],
'9a':   [3.0, 5.0, 'nan', 7.0, 6.0, 7.0, 0.0, 4.0, 7.0, 4.0, 'nan', 6.0, 4.0, 6.0, 5.0, 0.0, 4.0, 2.0, 5.0, 3.0, 7.0, 7.0, 7.0, 7.0, 6.0, 7.0, 6.0, 3.0, 1.0, 1.0, 7.0, 6.0, 1.0, 6.0, 5.0, 0.0, 6.0, 7.0, 4.0, 6.0, 2.0, 1.0, 4.0, 7.0, 6.0, 7.0, 5.0, 6.0, 7.0, 3.0, 7.0, 0.0, 6.0, 'nan', 2.0, 6.0, 2.0, 4.0, 1.0, 7.0],
'10a':  [5.0, 7.0, 'nan', 7.0, 7.0, 7.0, 2.0, 4.0, 7.0, 7.0, 2.0, 6.0, 6.0, 6.0, 6.0, 1.0, 3.0, 7.0, 0.0, 2.0, 7.0, 6.0, 7.0, 7.0, 7.0, 6.0, 2.0, 5.0, 'nan', 1.0, 7.0, 6.0, 6.0, 6.0, 4.0, 2.0, 2.0, 7.0, 1.0, 2.0, 6.0, 6.0, 6.0, 6.0, 7.0, 0.0, 1.0, 6.0, 7.0, 1.0, 7.0, 2.0, 6.0, 'nan', 6.0, 6.0, 2.0, 3.0, 3.0, 6.0],
'11a':  [0.0, 0.0, 'nan', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'nan', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'nan', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 'nan', 0.0, 0.0, 'nan', 0.0, 'nan', 0.0, 'nan', 0.0, 'nan', 0.0, 0.0, 'nan', 0.0],
'12a':  [0.0, 0.0, 'nan', 3.0, 1.0, 7.0, 0.0, 0.0, 2.0, 7.0, 'nan', 0.0, 4.0, 6.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 2.0, 0.0, 6.0, 6.0, 4.0, 2.0, 4.0, 0.0, 'nan', 4.0, 2.0, 0.0, 4.0, 3.0, 0.0, 2.0, 2.0, 7.0, 1.0, 0.0, 5.0, 3.0, 0.0, 2.0, 6.0, 0.0, 'nan', 2.0, 3.0, 'nan', 6.0, 'nan', 0.0, 'nan', 0.0, 'nan', 2.0, 3.0, 'nan', 0.0]}

# Removing empty lists & lists with all entries as 0        

# new_data = {k: v for k, v in data.items() if v and len(v)>0 and (not all(val==0 for val in v))}

data = pd.DataFrame(d_data) # change stop value to len(names) # dict to df

df2=data.replace("nan","") # to replace every 'nan' from df

"""
col_name = data.columns[(data == 0).all()] # finding the column with all 0 values
df2 = data.drop(col_name, axis=1) # delete the column with 0 values only
empty_col_rem = df2.dropna(axis=1,how='all') # drop columns with no values at all
"""

df2.to_csv("new_data_up.csv", index=False) # Write the DataFrame back to another CSV file

# n_data = pd.DataFrame(new_data, index=pd.RangeIndex(start=1, stop=len(data['Name'])+1, name='Roll No')) # change stop value to len(names) # dict to df
# n_data = pd.DataFrame(new_data) # change stop value to len(names) # dict to df

# n_data.to_csv('example2.csv', index=True)

print(time.time() - st)