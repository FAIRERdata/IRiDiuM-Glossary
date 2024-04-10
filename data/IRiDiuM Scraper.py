import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def extract_definitions_from_link(url):
    try:
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract term and definition
        term = soup.find('h1', id='firstHeading').text.strip()
        definition = soup.find('div', id='short-definition').text.strip()

        # Extract uuid
        uuid_meta_tag = soup.find('meta', attrs={'name': 'uuid'})
        uuid = uuid_meta_tag['content'] 
        
        # Extract source
        source_div = soup.find('div', id='extended')
        source = source_div.find('p').text

        # Check if definition is "n/a" and replace it with an empty string if it is
        if source.lower().strip() == "n/a":
            source = ""

        print(term)
        return term, definition, uuid, source
    except Exception as e:
        print(f"Error occurred with term at URL: {url}. Error: {e}")
        return None, None, None, None

def extract_definitions_from_category_page(url):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the specific section
    category_section = soup.find('div', class_='mw-category')
    
    # Find all links within the section
    links = category_section.find_all('a', href=True)

    # Extract definitions from each link
    definitions = []
    for link in links:
        link_url = link['href']
        if link_url.startswith('/web/'):  # Filter out non-relevant links
            term, definition, id, source = extract_definitions_from_link("https://web.archive.org" + link_url)
            definitions.append({'Term': term, 'Definition': definition, 'Definition Source': source, 'ID': id, 'Glossary Source': 'IRiDiuM v.1'})
    
    return definitions

# Example usage
url = 'https://web.archive.org/web/20180325125721/http://dictionary.casrai.org/Category:Research_Data_Domain'
definitions = extract_definitions_from_category_page(url)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(definitions)

# Save DataFrame to Excel
df.to_excel('IRiDiuM Raw Recovery.xlsx', index=False)