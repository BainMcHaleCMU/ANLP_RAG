import requests
from bs4 import BeautifulSoup
import re
import json
import time

# Utility function to clean up text by removing tabs, newlines, and excess spaces
def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()  # Remove tabs, newlines, and multiple spaces

# Function to scrape a specific event's detailed page (following "READ MORE" links if needed)
def scrape_event_details(event_url):
    response = requests.get(event_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    event_details = {}
    
    # Event title
    event_details['title'] = clean_text(soup.find('h1').text if soup.find('h1') else "No title")
    
    # Event date/time
    event_details['date_time'] = clean_text(soup.find('div', class_='eventdate').text if soup.find('div', class_='eventdate') else "No date")
    
    # Event location and venue
    venue_section = soup.find('div', class_='eventlocation')
    if venue_section:
        event_details['venue'] = clean_text(venue_section.find('strong').text if venue_section.find('strong') else "No venue")
        event_details['location'] = clean_text(venue_section.get_text(separator="\n").replace(event_details['venue'], '').strip())
    else:
        event_details['venue'] = "No venue"
        event_details['location'] = "No location"
    
    # Event external website
    event_website = soup.find('div', class_='eventlink')
    if event_website and event_website.find('a'):
        event_details['website'] = event_website.find('a')['href']
    else:
        event_details['website'] = "No website"
    
    # Extract event description (below venue or as additional content)
    description_paragraphs = soup.find_all('p')
    if description_paragraphs:
        event_details['description'] = clean_text(" ".join([p.text for p in description_paragraphs]))
    else:
        event_details['description'] = "No description"
    
    return event_details

# Function to scrape the main events listing page
def scrape_main_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    events = []
    
    # Find all event items on the page
    for event_div in soup.find_all('div', class_='eventitem'):
        event = {}
        
        # Extract title from the event's specific <h1> tag inside each event block
        event_title_tag = event_div.find('h1')
        event['title'] = clean_text(event_title_tag.text if event_title_tag else "No title")
                
        # Extract description from within the event block (removing other non-related content)
        description_div = event_div.find('div', class_='copyContent')
        if description_div:
            description_text = clean_text(description_div.get_text(separator=" ").strip())
            event['description'] = description_text.split(" READ MORE")[0]  # Stop at the "READ MORE" link text
        else:
            event['description'] = "No description"
        
        # Extract the "READ MORE" link and follow it to scrape more details
        read_more_link = event_div.find('a', class_='button green right')
        if read_more_link:
            read_more_url = f"https://downtownpittsburgh.com{read_more_link['href']}"
            event_details = scrape_event_details(read_more_url)
            
            # Merge the scraped event details with the main event data
            event.update(event_details)
        else:
            event['venue'] = "No venue"
            event['location'] = "No location"
            event['website'] = "No website"
        
        events.append(event)
        
        # Sleep to avoid overwhelming the server with requests
        time.sleep(1)
    
    return events

# Function to orchestrate scraping across multiple pages
def scrape_events_across_pages():
    base_urls = [
        "https://downtownpittsburgh.com/events/",
        "https://downtownpittsburgh.com/events/?n=11&y=2024",
        "https://downtownpittsburgh.com/events/?n=12&y=2024",
        "https://downtownpittsburgh.com/events/?n=1&y=2025"
    ]
    
    all_events = []
    for url in base_urls:
        print(f"Scraping events from {url}...")
        events = scrape_main_page(url)
        all_events.extend(events)
    
    # Save the events to a JSON file
    with open('downtown_pittsburgh_events.json', 'w', encoding='utf-8') as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)
    
    print(f"Scraped a total of {len(all_events)} events.")

if __name__ == "__main__":
    scrape_events_across_pages()
