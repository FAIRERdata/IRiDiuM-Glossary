###################################################
# Script name:    compilation.py
# Number lines:  55                      
# Version:           2024-04-11
# Software:         Python 3.12.2 (2024-02-06)
#                         Visual Studio Code (1.88.0)
# OS:                   Windows 11 Enterprise (2023-11-07, Build 22631.3296)
# Machine:          Dynabook Tecra
# Programmer:	  Esther Liu, ORCID ID https://orcid.org/0000-0001-9138-5986
# Validated by:  	Not validated
# Rcode licence:	None
# Data license:          None
# Purpose:  	       - Merge glossary data from IRiDiuM, RDC, CODATA, FAIR-Aware tool, NewTerms, Library and Archives Appendix3, and Library and Archives Appendix1.
# Cleaning:            - Define the column names to be source.column_name.
# Merging:             - Save the data to an Excel file.
###################################################
import os
import pandas as pd

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load each xlsx file into a separate DataFrame
df_iridium = pd.read_excel('IRiDiuM.xlsx')
df_rdc = pd.read_excel('RDC Glossary v2.0.xlsx')
df_codata = pd.read_excel('CODATA RDM Terminology 2023.xlsx')
df_fairer_aware = pd.read_excel('FAIR-Aware tool glossary.xlsx')
df_newterm = pd.read_excel('NewTerms.xlsx')
df_library3 = pd.read_excel('Library and Archives Appendix3.xlsx')
df_library1 = pd.read_excel('Library and Archives Appendix1.xlsx')

# Rename the columns of each DataFrame to prepend the source name to each column name, except for the "Term" column
df_iridium.columns = ['Term' if col=='Term' else 'IRiDiuM.'+col for col in df_iridium.columns]
df_rdc.columns = ['Term' if col=='PREFERRED TERM' else 'RDC.'+col for col in df_rdc.columns]
df_codata.columns = ['Term' if col=='Term' else 'CODATA.'+col for col in df_codata.columns]
df_fairer_aware.columns = ['Term' if col=='Term' else 'FAIRER-Aware.'+col for col in df_fairer_aware.columns]
df_newterm.columns = ['Term' if col=='Term' else 'NewTerm.'+col for col in df_newterm.columns]
df_library3.columns = ['Term' if col=='Term' else 'Library3.'+col for col in df_library3.columns]
df_library1.columns = ['Term' if col=='Term' else 'Library1.'+col for col in df_library1.columns]

# Perform a full outer join on all DataFrames on the "Term" column
df_merged = pd.merge(df_iridium, df_newterm, on='Term', how='outer')
df_merged = pd.merge(df_merged, df_rdc, on='Term', how='outer')
df_merged = pd.merge(df_merged, df_codata, on='Term', how='outer')
df_merged = pd.merge(df_merged, df_fairer_aware, on='Term', how='outer')
df_merged = pd.merge(df_merged, df_library3, on='Term', how='outer')
df_merged = pd.merge(df_merged, df_library1, on='Term', how='outer')

# Drop the 'FAIRER-Aware.Source' and 'RDC.TERMS (sort)' columns
df_merged = df_merged.drop(columns=['FAIRER-Aware.Source', 'RDC.TERMS (sort)'])

# Create the full path for the output file
output_file = os.path.join(script_dir, '..', 'merged_glossary.xlsx')

df_merged.to_excel(output_file, index=False)