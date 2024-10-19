import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

# Function to extract event details from event page
def extract_event_details(event_url):
    try:
        response = requests.get(event_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Example selector for event description (adjust based on actual structure)
        description = soup.select_one("your-event-description-selector").text.strip()  # Replace with actual CSS selector
        return description
    except Exception as e:
        print(f"Failed to fetch details for {event_url}: {e}")
        return None

# Start date and end date
start_date = datetime(2024, 10, 27)
end_date = datetime(2025, 5, 31)

# Iterate over the date range
current_date = start_date
while current_date <= end_date:
    formatted_date = current_date.strftime('%Y%m%d')
    url = f"https://events.cmu.edu/day/date/{formatted_date}"
    
    try:
        # Fetch the page for the current date
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find and extract event links (adjust based on actual HTML structure)
        events = soup.select(".lw_cal_event .lw_events_title a")
        
        if events:
            for event in events:
                event_link = event['href']
                event_title = event.text.strip()
                print(f"Event: {event_title}, Link: {event_link}")

                # Optionally extract event details
                description = extract_event_details(event_link)
                if description:
                    print(f"Description: {description}")
        else:
            print(f"No events found for {formatted_date}")
    
    except Exception as e:
        print(f"Failed to scrape {formatted_date}: {e}")

    # Move to the next date
    current_date += timedelta(days=1)
    time.sleep(1)  # Sleep between requests to avoid overloading the server

print("Scraping completed.")
