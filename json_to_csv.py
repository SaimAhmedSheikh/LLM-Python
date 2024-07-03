import pandas as pd
 
df = pd.read_json('results.json')

df_cleaned = df.drop_duplicates(subset=['Parameter'])
# Write the DataFrame to a CSV file
df_cleaned.to_csv('results.csv', index=False)
