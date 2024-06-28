import pandas as pd
 
df = pd.read_json('summaries.json')

# df_cleaned = df.drop_duplicates(subset=['test'])
# Write the DataFrame to a CSV file
df.to_csv('result_data.csv', index=False)
