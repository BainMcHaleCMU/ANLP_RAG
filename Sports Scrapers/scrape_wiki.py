import requests
from bs4 import BeautifulSoup
import json
import re

# Wikipedia URLs
urls = [
    'https://en.wikipedia.org/wiki/Pittsburgh_Pirates',
    'https://en.wikipedia.org/wiki/Pittsburgh_Steelers',
    'https://en.wikipedia.org/wiki/Pittsburgh_Penguins'
]

# Function to clean up the text while preserving punctuation and spacing
def clean_text(text):
    # Remove Wikipedia-style citation references like [113]
    text = re.sub(r'\[\d+\]', '', text)  # Remove citation markers like [113]
    
    # Ensure spacing and punctuation are preserved
    text = re.sub(r'(?<=[.,!?;:])(?=[^\s])', ' ', text)  # Add space after punctuation if needed
    text = re.sub(r'\s+', ' ', text)  # Collapse multiple spaces into one
    
    return text.strip()

# Function to parse Wikipedia page and extract all <p> tags as description
def parse_wikipedia_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Get the title of the page
            page_title = soup.find('h1', {'id': 'firstHeading'}).get_text()

            # Extract all paragraphs (<p> tags)
            paragraphs = soup.find_all('p')
            description = " ".join([clean_text(p.get_text()) for p in paragraphs])

            # Return the result as a dictionary
            return {
                "title": page_title,
                "description": description
            }
        else:
            print(f"Failed to retrieve {url}: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error while scraping {url}: {e}")
        return None

# List to store data for all pages
all_data = []

# Parse each Wikipedia URL
for url in urls:
    print(f"Scraping: {url}")
    parsed_data = parse_wikipedia_page(url)
    if parsed_data:
        all_data.append(parsed_data)

# Output data to a JSON file
with open('sports_wikipedia.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print("Scraping complete. Data saved to wikipedia_scraped_data.json")
