###################################################
# Script name:    Appendix 3 Scraper.py
# Number lines:  83                       
# Version:           2024-04-11
# Software:         Python 3.12.2 (2024-02-06)
#                         Visual Studio Code (1.88.0)
# OS:                   Windows 11 Enterprise (2023-11-07, Build 22631.3296)
# Machine:          Dynabook Tecra
# Programmer:	  Esther Liu, ORCID ID https://orcid.org/0000-0001-9138-5986
# Validated by:  	Not validated
# Rcode licence:	None
# Data license:          None
# Purpose:  	       - Scrape data by term, definition, purpose, and comment from Appendix 3 of the Library and Archives Canada website.
# Cleaning:            - combines the 'Comment' and 'Definition' columns into a single 'Definition' column
#                      - prepends "The purpose is " to the 'Purpose' column and changes the first letter to lowercase
#                      - drops the 'Comment' column
# Merging:             - Save the data to an Excel file.
###################################################
from bs4 import BeautifulSoup, NavigableString
import requests
import pandas as pd
import os

url = "https://library-archives.canada.ca/eng/services/government-canada/information-disposition/managing-government-records/guidelines-information-management/Pages/operational-standard-digital-archival-records-metadata.aspx"

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

# Find the section between <h2 id="appa"> and <h2 id="appb">
start = soup.find(id="appc")
end = soup.find(id="appd")

section_html = []
for sibling in start.find_next_siblings():
    if sibling == end:
        break
    if sibling.name:  # only append tags, not strings
        section_html.append(str(sibling))

# Parse the section with BeautifulSoup
section = BeautifulSoup(''.join(section_html), 'html.parser')
print(section.prettify())

# Find all <h3> tags in the section
terms = section.find_all('h3')

data = []
for term in terms:
    # Get the term text
    term_text = term.get_text(strip=True)
    
    # Find the next <table> tag
    table = term.find_next('table')
    
    # Get the texts of the <td> tags as the definition, purpose, and comment
    tds = table.find_all('td')
    definition = tds[0].get_text(strip=True) if len(tds) > 0 else None
    purpose = tds[1].get_text(strip=True) if len(tds) > 1 else None
    comment = tds[4].get_text(strip=True) if len(tds) > 4 else None
    
    # Append the data to the list
    data.append([term_text, definition, purpose, comment])

# Create a DataFrame and write it to an Excel file
df = pd.DataFrame(data, columns=['Term', 'Definition', 'Purpose', 'Comment'])

# Append the comment to the definition
df['Definition'] = df['Definition'] + ' ' + df['Comment']

# Prepend "The purpose is " to the purpose and change the first letter to lowercase
df['Purpose'] = 'The purpose is ' + df['Purpose'].str[0].str.lower() + df['Purpose'].str[1:]

# Drop the 'Comment' column
df = df.drop(columns='Comment')

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the full path for the output file
output_file = os.path.join(script_dir,'..', 'Library and Archives Appendix3.xlsx')

df.to_excel(output_file, index=False)