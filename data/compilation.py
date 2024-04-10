import os
import pandas as pd

# Change the working directory to the location of your data files
os.chdir('c:/Users/LiuEs/Desktop/glossary/data/')

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

# Save the merged DataFrame to a new xlsx file
df_merged.to_excel('merged_glossary.xlsx', index=False)