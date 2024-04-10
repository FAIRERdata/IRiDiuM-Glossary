from flask import Flask, render_template
import pandas as pd
import os

# Change the working directory to the location of your data files
os.chdir('c:/Users/LiuEs/Desktop/glossary/')

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
    rendered_html = render_template('glossary.html', glossary_entries=glossary_entries, first_terms=first_terms)

    # Ensure the 'docs' folder exists
    if not os.path.exists('docs'):
        os.makedirs('docs')

    # Save the rendered HTML to 'docs/index.html'
    with open('docs/glossary.html', 'w') as f:
        f.write(rendered_html)

    return 'Static HTML file generated successfully'

if __name__ == '__main__':
    app.run(debug=True)
