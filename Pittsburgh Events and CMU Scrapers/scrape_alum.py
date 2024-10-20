import requests
from bs4 import BeautifulSoup
import json
import time

# List of URLs to scrape
urls = [
    "https://www.cmu.edu/engage/alumni/events/campus/index.html",
    "https://www.cmu.edu/engage/alumni/events/campus/spring-carnival/index.html",
    "https://www.cmu.edu/engage/alumni/events/campus/spring-carnival/highlights.html",
    "https://www.springcarnival.org/booth.shtml",
    "https://cmubuggy.org/",
    "https://www.snstheatre.org/",
    "https://activitiesboard.org/",
    "https://www.cmu.edu/engage/alumni/events/campus/homecoming/index.html",
    "https://www.cmu.edu/engage/alumni/events/campus/homecoming/schedule.html",
    "https://www.cmu.edu/engage/alumni/events/campus/reunions/index.html",
    "https://www.cmu.edu/engage/alumni/events/campus/alumni-awards/index.html",
    "https://www.cmu.edu/engage/alumni-awards-recipients/index.html"
]

# List to store the scraped data
scraped_data = []

# Function to clean and extract text
def scrape_page(url):
    try:
        # Skip SSL verification for pages that cause SSL errors
        response = requests.get(url, timeout=10, verify=False) if "springcarnival.org" in url else requests.get(url, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title from h1
            h1_tag = soup.find('h1')
            title = h1_tag.get_text(strip=True) if h1_tag else "No Title"

            # Extract all visible text from the page
            text = ' '.join(soup.stripped_strings)

            # Store the result as a dictionary
            scraped_data.append({
                "title": title,
                "text": text
            })

        else:
            print(f"Failed to fetch {url}: {response.status_code}")

    except Exception as e:
        print(f"Error while scraping {url}: {e}")

# Scrape each URL in the list
for url in urls:
    scrape_page(url)
    time.sleep(1)  # Sleep for 1 second between requests to avoid overloading the server

# Save the scraped data to a JSON file
with open('scraped_cmu_alumni_events.json', 'w', encoding='utf-8') as f:
    json.dump(scraped_data, f, ensure_ascii=False, indent=2)

print(f"Scraped {len(scraped_data)} pages.")
