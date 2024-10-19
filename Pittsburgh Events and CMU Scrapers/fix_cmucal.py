import json
import re
from datetime import datetime

def clean_description(description):
    # Replace HTML-encoded ampersand with actual "and"
    description = description.replace("&amp;", "and")
    # Remove any remaining HTML tags or excessive spaces/newlines
    description = re.sub(r'<.*?>', '', description)
    description = re.sub(r'\s+', ' ', description).strip()
    return description

def clean_title(title):
    # Replace HTML-encoded ampersand with actual "and"
    title = title.replace("&amp;", "and")
    return title

def fix_event_data(events):
    cleaned_events = []
    for event in events:
        # Fix date format
        event_date = datetime.strptime(event['date'], '%Y%m%d').strftime('%Y-%m-%d')
        
        # Handle time range or missing end time
        if "(End time not available)" in event['time_range']:
            start_time = event['time_range'].split()[0]
            event_time = f"{start_time}"
        else:
            event_time = event['time_range'].replace(' to ', ' - ')

        # Clean description and other fields
        cleaned_event = {
            'date': event_date,
            'date_time': event_time,
            'title': clean_title(event['title']),
            'description': clean_description(event['description']),
            'location': event['location']
        }
        cleaned_events.append(cleaned_event)
    
    return cleaned_events

# Load the provided JSON file
with open('extracted_cmu_events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

# Process and clean the events
cleaned_events = fix_event_data(events)

# Save the cleaned events to a new JSON file
with open('cmu_calendar_events.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_events, f, ensure_ascii=False, indent=2)

print("Events data cleaned and saved successfully!")
