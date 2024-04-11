###################################################
# Script name:    Appendix 1 Scraper.py
# Number lines:  86                       
# Version:           2024-04-11
# Software:         Python 3.12.2 (2024-02-06)
#                         Visual Studio Code (1.88.0)
# OS:                   Windows 11 Enterprise (2023-11-07, Build 22631.3296)
# Machine:          Dynabook Tecra
# Programmer:	  Esther Liu, ORCID ID https://orcid.org/0000-0001-9138-5986
# Validated by:  	Not validated
# Rcode licence:	None
# Data license:          None
# Purpose:  	       - Scrape data by term, French term, definition, and footnote from Appendix 1 of the Library and Archives Canada website.
# Cleaning:            - Remove unnecessary characters and formatting.
#                      - Combines definition parts across multiple HTML elements.
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
start = soup.find(id="appa")
end = soup.find(id="appb")

section_html = []
for sibling in start.find_next_siblings():
    if sibling == end:
        break
    if sibling.name:  # only append tags, not strings
        section_html.append(str(sibling))

# Parse the section with BeautifulSoup
section = BeautifulSoup(''.join(section_html), 'html.parser')

data = []
term = french_term = definition = footnote = None
definition_parts = []
for sibling in start.find_next_siblings():
    if sibling == end:
        break
    if sibling.name == 'p' and sibling.b:
        # If a term was found previously, add the term and the collected definition to the data
        if term is not None:
            definition = ' '.join(definition_parts)
            data.append([term, french_term, definition, footnote])
            definition_parts = []  # reset definition parts
        term = sibling.b.get_text(strip=True)
        if sibling.b.i:
            french_term = sibling.b.i.get_text(strip=True).strip('[]')
            term = term.replace('['+french_term+']', '')  # remove the French term from the term
    elif term is not None:
        # If a term has been found, add the text of the sibling to the definition
        definition_parts.append(sibling.get_text(strip=True))
        footnote_links = sibling.find_all('a', {'class': 'fn-lnk'})
        footnotes = []
        for footnote_link in footnote_links:
            footnote_id = footnote_link['href'].lstrip('#')
            footnote_tag = soup.find(id=footnote_id)
            if footnote_tag:
                footnotes.append(footnote_tag.get_text(strip=True))
        footnote = '; '.join(footnotes) if footnotes else None

# Add the last term and definition to the data
if term is not None:
    definition = ' '.join(definition_parts)
    data.append([term, french_term, definition, footnote])

print(f"Extracted {len(data)} rows of data.")
df = pd.DataFrame(data, columns=['Term', 'French Term', 'Definition', 'Footnote'])

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the full path for the output file
output_file = os.path.join(script_dir,'..', 'Library and Archives Appendix1.xlsx')

df.to_excel(output_file, index=False)