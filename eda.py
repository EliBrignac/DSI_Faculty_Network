import pandas as pd


df1 = pd.read_csv('ud_faculty_scholar_basic_info.csv')
df2 = pd.read_csv('ud_faculty_scholar_publications.csv')
print(df1.head())
print(df2.head())
import pandas as pd

# Assuming df1 is the first DataFrame with scholar information
# and df2 is the second DataFrame with publication details.

df2 = df2.merge(df1, left_on='Author Name', right_on='Name', how='left')

# Drop the redundant 'Name' column from df1 (if necessary)
df2.drop(columns=['Name'], inplace=True)


df3 = pd.read_csv('ud_dsi_faculty.csv')


df2 = df2.merge(df3, left_on='Author Name', right_on='Name', how='left')

df2.to_csv('ud_faculty_joined.csv', index=False)






