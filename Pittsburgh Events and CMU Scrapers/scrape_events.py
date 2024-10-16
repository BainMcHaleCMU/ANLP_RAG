import requests
from bs4 import BeautifulSoup
import re
import time
import json

# Utility function to clean up text by removing tabs, newlines, and excess spaces
def clean_text(text):
    if not text:
        return ""
    # Remove tabs, newlines, and reduce multiple spaces to a single space
    return re.sub(r'\s+', ' ', text).strip()

# Function to extract all text content for events
def extract_events(soup):
    events = []
    
    # Loop through each event in the 'date-row' class
    for event_li in soup.find_all('li', class_='date-row'):
        
        # Extract the date information
        month = clean_text(event_li.find('div', class_='month').text if event_li.find('div', class_='month') else "No month")
        day = clean_text(event_li.find('div', class_='day').text if event_li.find('div', class_='day') else "No day")
        year = clean_text(event_li.find('div', class_='year').text if event_li.find('div', class_='year') else "No year")
        date = f"{month} {day}, {year}"
        
        # Extract time and weekday information
        time = clean_text(event_li.find('div', class_='time').text.strip() if event_li.find('div', class_='time') else "No time")
        
        # Extract description (event name)
        description = clean_text(event_li.find('div', class_='venue').find('div').text if event_li.find('div', class_='venue') else "No description")
        
        # Extract venue (location name)
        venue = clean_text(event_li.find('div', class_='date-desc').text if event_li.find('div', class_='date-desc') else "No venue")
        
        # Extract the location (city and state)
        location = clean_text(event_li.find('span', class_='location').get_text(separator="\n").strip() if event_li.find('span', class_='location') else "No location")
        
        # Extract the price information
        price = clean_text(event_li.find('div', class_='from-price').text.strip() if event_li.find('div', class_='from-price') else "No price")

        # Add the extracted data to the list of events
        events.append({
            'date': date,
            'time': time,
            'description': description,  # Now storing the description
            'venue': venue,  # Now storing the venue separately
            'location': location,
            'price': price
        })
    
    return events

# Function to load more events using the pagenum-based URL for pagination
def load_more_events(base_url, page_number):
    paginated_url = f"{base_url}?pagenum={page_number}"
    response = requests.get(paginated_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract events from the newly loaded content
    return extract_events(soup)

# Function to scrape events for a specific month across all pages
def scrape_month_page(base_url):
    page_number = 1
    events = []

    while True:
        print(f"Scraping {base_url}, Page {page_number}")
        more_events = load_more_events(base_url, page_number)

        # Stop if no more events are returned
        if not more_events:
            break
        
        events.extend(more_events)
        page_number += 1
        time.sleep(1)  # Delay to avoid overwhelming the server

    return events

# Function to extract the month-specific URLs from the homepage
def scrape_homepage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links corresponding to months using a regex pattern for month names
    month_links = []
    month_pattern = re.compile(r'(january|february|march|april|may|june|july|august|september|october|november|december)', re.IGNORECASE)
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        if month_pattern.search(href):  # Match any month in the URL
            month_links.append(href)
    
    return month_links

# Main function to orchestrate the scraping across all months
def main():
    base_url = 'https://pittsburgh.events/'  # Replace with actual homepage URL

    # Step 1: Scrape the homepage for month-specific links
    month_urls = scrape_homepage(base_url)

    # Step 2: Loop through each month and scrape events
    all_events = []
    for month_url in month_urls:
        print(f"Scraping events for {month_url}...")
        events = scrape_month_page(month_url)
        all_events.extend(events)

    # Save all events to a JSON file
    with open('pittsburgh_events.json', 'w', encoding='utf-8') as f:
        json.dump(all_events, f, ensure_ascii=False)

    print(f"Scraped a total of {len(all_events)} events across all months.")

if __name__ == "__main__":
    main()
