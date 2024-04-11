###################################################
# Script name:    data_cleansing.py
# Number lines:  94                       
# Version:           2024-04-11
# Software:         Python 3.12.2 (2024-02-06)
#                         Visual Studio Code (1.88.0)
# OS:                   Windows 11 Enterprise (2023-11-07, Build 22631.3296)
# Machine:          Dynabook Tecra
# Programmer:	  Esther Liu, ORCID ID https://orcid.org/0000-0001-9138-5986
# Validated by:  	Not validated
# Rcode licence:	None
# Data license:          None
# Purpose:  	       - Clean data from IRiDiuM Raw Recovery.xlsx and RDC Raw.xlsx
# Cleaning:            - IRiDiuM: Split the "Definition Source" column into "Long Definition" and "Reference" columns
#                      - IRiDiuM: Split the "Definition" column into "Short Definition", "Synonym", and "Related Term" columns
#                      - IRiDiuM: merge with the old and drop the old 'Definition' and 'Definition Source' columns.
#                      - RDC 2.0: Remove the leading "SYNONYM.", "ACRONYM.", and "RELATED TERM." in the respective columns
# Merging:             - Save both the cleaned data to Excel files.
###################################################

import os
import pandas as pd
from openpyxl import load_workbook

#-----------------------------------------------------------#
#------------------------- IRiDiuM -------------------------#
#-----------------------------------------------------------#

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

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

# Remove leading and trailing spaces from each column in new_df1
for col in new_df1.columns:
    new_df1[col] = new_df1[col].str.strip()

# Remove leading and trailing spaces from each column in new_df2
for col in new_df2.columns:
    new_df2[col] = new_df2[col].str.strip()

# Join the new DataFrames with the original one
df = df.join(new_df1).join(new_df2)

# Drop the old "Definition" and "Definition Source" columns
df = df.drop(columns=['Definition', 'Definition Source'])

# Rearrange the columns
df = df[['Term', 'Short Definition', 'Long Definition', 'Reference', 'Synonym', 'Related Term', 'ID']]

# Create the full path for the output file
output_file = os.path.join(script_dir, '..', 'IRiDiuM.xlsx')

df.to_excel(output_file, index=False)

#-----------------------------------------------------------#
#------------------------- RDC 2.0 -------------------------#
#-----------------------------------------------------------#

# Read the Excel file
df = pd.read_excel('RDC Raw.xlsx', engine='openpyxl')

# Remove the leading "SYNONYM." in the "SYNONYMS" column
df['SYNONYMS'] = df['SYNONYMS'].str.replace('^SYNONYM. ', '', regex=True)

# Remove the leading "ACRONYM." in the "ACRONYMS" column
df['ACRONYMS'] = df['ACRONYMS'].str.replace('^ACRONYM. ', '', regex=True)

# Remove the leading "RELATED TERM." in the "RELATED TERMS" column
df['RELATED TERMS'] = df['RELATED TERMS'].str.replace('^RELATED TERM. ', '', regex=True)

# Create the full path for the output file
output_file = os.path.join(script_dir, '..', 'RDC Glossary.xlsx')

df.to_excel(output_file, index=False)