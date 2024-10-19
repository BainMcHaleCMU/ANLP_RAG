import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def setup_session():
    session = requests.Session()
    retries = Retry(
        total=5,  # Retry up to 5 times
        backoff_factor=2,  # Exponential backoff: wait 2^retry seconds
        status_forcelist=[500, 502, 503, 504, 524, 550],
        allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated from 'method_whitelist' to 'allowed_methods'
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    # Add headers like a common web browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    return session

session = setup_session()

# Utility function to clean up text by removing tabs, newlines, and excess spaces
def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

# Function to scrape events from the main search results page
def scrape_events_on_page(url):
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        events = []

        # Find all event items (main page events list)
        for event_li in soup.find_all('li', class_='fdn-pres-item'):
            event = {}

            # Event title
            title_tag = event_li.find('p', class_='fdn-teaser-headline')
            if title_tag and title_tag.find('a'):
                event['title'] = clean_text(title_tag.find('a').text)
            else:
                event['title'] = "No title"  # Fallback if not found

            # Event date
            event_date = event_li.find('p', class_='fdn-teaser-subheadline')
            event['date'] = clean_text(event_date.text if event_date else "No date")

            # Event description
            description_div = event_li.find('div', class_='fdn-teaser-description')
            event['description'] = clean_text(description_div.text if description_div else "No description")

            # Event venue and location
            venue_tag = event_li.find('a', class_='fdn-event-teaser-location-link')
            event['venue'] = clean_text(venue_tag.text if venue_tag else "No venue")
            location_span = event_li.find('span', class_='uk-text-muted')
            event['location'] = clean_text(location_span.text if location_span else "No location")

            # Event external link for tickets (if available)
            ticket_link = event_li.find('a', class_='fdn-teaser-ticket-link')
            event['ticket_url'] = ticket_link['href'] if ticket_link else "No ticket link"

            # Add the event to the events list
            if event['title'] != "No title":
                events.append(event)

            # Delay between requests (use random delay to avoid detection)
            time.sleep(random.uniform(1, 3))  # Random delay between 1-3 seconds

    except requests.exceptions.RequestException as e:
        print(f"Failed to scrape {url}: {e}")
        return []

    return events

# Function to handle pagination and scrape all event pages
def scrape_all_events():
    base_url = "https://www.pghcitypaper.com/pittsburgh/EventSearch"
    params = {
        "narrowByDate": "2024-10-27-to-2025-09-30",
        "page": 1,
        "sortType": "date",
        "v": "d"
    }

    # Fetch the first page to determine the total number of pages
    first_page_url = f"{base_url}?narrowByDate={params['narrowByDate']}&page={params['page']}&sortType={params['sortType']}&v={params['v']}"
    first_page_response = session.get(first_page_url)
    first_page_soup = BeautifulSoup(first_page_response.content, 'html.parser')

    # Find the total number of pages in the pagination section
    pagination_section = first_page_soup.find('p', class_='uk-text-right uk-margin-remove fdn-search-result-header')
    if pagination_section:
        pagination_spans = pagination_section.find_all('span')
        if len(pagination_spans) > 1:
            total_pages_text = pagination_spans[1].text.strip()  # 'of 19'
            total_pages = int(total_pages_text.split(' ')[1])  # Extract '19' and convert to integer
    else:
        total_pages = 1  # Fallback if pagination info isn't found

    print(f"Total pages to scrape: {total_pages}")

    all_events = []

    while params['page'] <= total_pages:
        url = f"{base_url}?narrowByDate={params['narrowByDate']}&page={params['page']}&sortType={params['sortType']}&v={params['v']}"
        print(f"Scraping events from {url}...")
        events_on_page = scrape_events_on_page(url)
        all_events.extend(events_on_page)
        params['page'] += 1

    # Save the events to a JSON file
    with open('pgh_paper_events.json', 'w', encoding='utf-8') as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)

    print(f"Scraped a total of {len(all_events)} events.")

if __name__ == "__main__":
    scrape_all_events()
