import pandas as pd
 
# r -> Raw Data It will exclude the backslash. Its like it will omit \t \n
source_path = r"C:\Users\suganya\Downloads\test_Gs (1).csv"  
export_path = r"C:\Users\suganya\Downloads\sample.csv"  
 
# FIX: Added encoding='latin1' to handle special characters smoothly
df = pd.read_csv(source_path, nrows=30, encoding='latin1')  # dataframe ah store pannudhu
df.to_csv(export_path, index=False) #store panna df ah seperate csv file la store pannudhu
 
print(f"Exported {len(df)} rows to: {export_path}")