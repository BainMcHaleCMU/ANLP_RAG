import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# List of User-Agents to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/18.17763',
    # Add more user agents as needed
]

def setup_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=2,  # Exponential backoff
        status_forcelist=[500, 502, 503, 504, 524, 550],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

session = setup_session()

# Utility function to clean up text by removing tabs, newlines, and excess spaces
def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

# Function to rotate User-Agent
def rotate_user_agent():
    return random.choice(USER_AGENTS)

# Function to scrape events from a single page with retries and delay
def scrape_events_on_page(url, page_num):
    try:
        session.headers.update({
            'User-Agent': rotate_user_agent()
        })
        response = session.get(url, timeout=15)
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
                event['title'] = "No title"

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

            # Only add the event if it has a valid title
            if event['title'] != "No title":
                events.append(event)

            # Delay between requests
            time.sleep(random.uniform(1, 3))

        return events

    except requests.exceptions.RequestException as e:
        print(f"Failed to scrape page {page_num} ({url}): {e}")
        return None

# Function to scrape specific problematic pages with larger delays and retries
def scrape_specific_pages():
    base_url = "https://www.pghcitypaper.com/pittsburgh/EventSearch"
    params = {
        "narrowByDate": "2024-10-27-to-2025-09-30",
        "sortType": "date",
        "v": "d"
    }
    
    # List of problematic pages to scrape
    pages_to_scrape = [7, 8, 9, 11, 12, 13, 14, 16, 17]
    
    all_events = []

    for page in pages_to_scrape:
        params['page'] = page
        url = f"{base_url}?narrowByDate={params['narrowByDate']}&page={params['page']}&sortType={params['sortType']}&v={params['v']}"
        print(f"Scraping events from {url}...")
        
        success = False
        retries = 0
        
        while not success and retries < 5:
            events_on_page = scrape_events_on_page(url, params['page'])
            if events_on_page is not None:
                all_events.extend(events_on_page)
                success = True
            else:
                retries += 1
                if retries < 5:
                    print(f"Retrying page {page}... attempt {retries}")
                else:
                    print(f"Page {page} could not be scraped")
                time.sleep(10)  # Wait before retrying

    # Save the scraped events to a separate JSON file for these specific pages
    with open('pgh_paper_more_events.json', 'w', encoding='utf-8') as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)

    print(f"Scraped a total of {len(all_events)} events from specific pages.")

if __name__ == "__main__":
    scrape_specific_pages()
