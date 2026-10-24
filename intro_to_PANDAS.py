# PANDAS => Panel Datas

from tokenize import group
import pandas as pd

data = [100, 200, 300]
series1 = pd.Series(data)    # Here, Series() is a constructor -> It converts into a 1d array

series2 = pd.Series(data, index = ['a', 'b', 'c'])

ind = series2.loc['a']  # loc -> location,  iloc -> gives the integer location ie index pos 
greater_than_200 = series1[series1 >= 200]      # subset property

# print(ind)
# print(series1)
# print(series2)
# print(greater_than_200)

# by using dictionary, We can map Key -> Index and Value -> Series data
d = {"A":1, "B":2, 'C':3}
series_d = pd.Series(d)

# print(series_d)

# Data Frame => Rows and Columns
d = {
    "Name": ['Suganya', 'Venkat', 'Tamil', 'Priyanka', 'Akila'],
    "Age": [20, 23, 24, 22, 23]
}

df = pd.DataFrame(d)

# Adding a column
df['Experience'] = [0, 4, 4, 1, 2]

# Add a new Row
newRow = pd.DataFrame([{'Name': 'NewOne', 'Age': 25, 'Experience':5}])
df = pd.concat([df, newRow])

# print(df)

# From the File
df_csv = pd.read_csv("formatted.csv")   # index_col
# print(df_csv)   # first and last 5 rows gets printed
# To print everything, Use df.to_string

#SELECTION BY COLUMN
column = df['Name']

#SELECTION BY ROW
row = df.loc[0] # U can also use .iloc[start:end]
# print(row)

# try => risky code
# except => exceutes when error occurs
# else => executes only if the try block executes ( no errors )
# finally => runs for sure

#Filtering  Subscript operator -> []
    # filtering is nothing but creating a separate dataframe with required needs

India = df_csv[df_csv["country"] == 'India']
# print(India)

# In pandas, Use & for and, | for or

# AGGREGATE => df.mean() df.sum() df.min df.max() df.count() 
    # If you want to pass a single column, use df["column_name"].mean()

# GROUP BY

grp = df_csv.groupby("country")
# print(grp.max())

# Data Cleaning
    # Process of fixing/removing the incomplete, incorrect data
    # df.drop()

# None or Missing
missing_country = df_csv.dropna(subset=["country"])
print(missing_country.to_string())