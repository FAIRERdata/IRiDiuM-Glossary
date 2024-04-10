import os
import pandas as pd
from openpyxl import load_workbook

#-----------------------------------------------------------#
#------------------------- IRiDiuM -------------------------#
#-----------------------------------------------------------#

# Change the working directory to the location of your data files
os.chdir('c:/Users/LiuEs/Desktop/glossary/glossary_files/')

# Read the Excel file
df = pd.read_excel('IRiDiuM Raw Recovery.xlsx', engine='openpyxl')

# Split the "Definition Source" column
new_df1 = df['Definition Source'].str.split('REFERENCE.', expand=True)

# Assign the column names
new_df1.columns = ["Long Definition", "Reference"]

# Split the "Definition" column
new_df2 = df['Definition'].str.split('\\[\\[Short definition::|SYNONYM.|RELATED TERM.', expand=True)

# Check the number of columns generated
num_cols = len(new_df2.columns)

# Create a list of column names based on the number of columns
col_names = ["Short Definition", "Synonym", "Related Term"][:num_cols]

# Assign the column names
new_df2.columns = col_names

# Fill NaN values
new_df1 = new_df1.fillna('')
new_df2 = new_df2.fillna('')

# Remove leading and trailing spaces from each column in new_df1
for col in new_df1.columns:
    new_df1[col] = new_df1[col].str.strip()

# Remove leading and trailing spaces from each column in new_df2
for col in new_df2.columns:
    new_df2[col] = new_df2[col].str.strip()

# Join the new DataFrames with the original one
df = df.join(new_df1).join(new_df2)

# Replace all "n/a" values with an empty string
df = df.replace('n/a', '')

# Drop the old "Definition" and "Definition Source" columns
df = df.drop(columns=['Definition', 'Definition Source'])

# Rearrange the columns
df = df[['Term', 'Short Definition', 'Long Definition', 'Reference', 'Synonym', 'Related Term', 'ID']]

# Write the DataFrame back to an Excel file
df.to_excel('IRiDiuM.xlsx', index=False)

#-----------------------------------------------------------#
#------------------------- RDC 2.0 -------------------------#
#-----------------------------------------------------------#

# Read the Excel file
df = pd.read_excel('RDC Glossary v2.0.xlsx', engine='openpyxl')

# Remove the leading "SYNONYM." in the "SYNONYMS" column
df['SYNONYMS'] = df['SYNONYMS'].str.replace('^SYNONYM. ', '', regex=True)

# Remove the leading "ACRONYM." in the "ACRONYMS" column
df['ACRONYMS'] = df['ACRONYMS'].str.replace('^ACRONYM. ', '', regex=True)

# Remove the leading "RELATED TERM." in the "RELATED TERMS" column
df['RELATED TERMS'] = df['RELATED TERMS'].str.replace('^RELATED TERM. ', '', regex=True)

# Write the DataFrame back to an Excel file
df.to_excel('RDC Glossary v2.0.xlsx', index=False)