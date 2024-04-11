###################################################
# Script name:    data_api.py
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
# Purpose:  	       - Read data from an Excel file, convert it to a list of dictionaries, and render a Static HTML template.
# Merging:             - Generate a Static HTML file.
###################################################

from flask import Flask, render_template
import pandas as pd
import os

# Get the directory of the current script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

@app.route('/')
def glossary():
    # Read data from Excel file
    df = pd.read_excel('data/IRiDiuM.xlsx')

    # Convert DataFrame to list of dictionaries
    glossary_entries = df.where(pd.notnull(df), '').to_dict(orient='records')

    # Create a dictionary that maps each letter to the first term that starts with that letter
    first_terms = {}
    for entry in glossary_entries:
        first_letter = entry['Term'][0].lower()
        if first_letter not in first_terms:
            first_terms[first_letter] = entry['Term']

    # Render the index.html template
    rendered_html = render_template('template.html', glossary_entries=glossary_entries, first_terms=first_terms)

    # Ensure the 'docs' folder exists
    if not os.path.exists('docs'):
        os.makedirs('docs')

    # Save the rendered HTML to 'docs/index.html'
    with open('docs/index.html', 'w') as f:
        f.write(rendered_html)

    return 'Static HTML file generated successfully'

if __name__ == '__main__':
    app.run(debug=True)