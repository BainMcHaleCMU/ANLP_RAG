import requests
from bs4 import BeautifulSoup
import json
import re

# Function to clean and replace any \u followed by 4 characters with whitespace
def clean_text(text):
    # List of escape sequences to remove
    escape_sequences = [
        '\u00c2', '\u00a0', '\u00e2', '\u0080', '\u0099', 
        '\u00ef', '\u00ac', '\u0081', '\u00fb'
    ]
    
    # Replace each escape sequence with an empty string
    for seq in escape_sequences:
        text = text.replace(seq, ' ')

    text = text.replace("\ufb00", "ff")
    text = re.sub(r'\s+', ' ', text)

    # Return cleaned text
    return text.strip()

def clean_text_2(text):
    # Remove extra spaces, newlines, and non-breaking spaces
    return ' '.join(text.split()).replace('\xa0', ' ')

def clean_text_3(text):
    return text.strip().replace('\n', '').replace('\t', '')

# Function to scrape player roster
def scrape_players_roster(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    roster_data = []

    # Locate all roster sections by iterating over the tables
    roster_sections = soup.find_all('div', {'class': 'nfl-o-roster'})
    
    for section in roster_sections:
        status = section.find('span', {'class': 'nfl-o-roster__title-status'}).get_text(strip=True)
        table = section.find('table', {'class': 'd3-o-table'})
        
        if table:
            rows = table.find('tbody').find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 1:
                    name = cells[0].find('span', {'class': 'nfl-o-roster__player-name'}).get_text(strip=True)
                    number = cells[1].get_text(strip=True)
                    position = cells[2].get_text(strip=True)
                    height = cells[3].get_text(strip=True).replace(' ', '')
                    weight = cells[4].get_text(strip=True)
                    age = cells[5].get_text(strip=True)
                    experience = cells[6].get_text(strip=True)
                    college = cells[7].get_text(strip=True)
                    roster_data.append({
                        'name': name,
                        'number': number,
                        'position': position,
                        'height': height,
                        'weight': weight,
                        'age': age,
                        'experience': experience,
                        'college': college,
                        'status': status  # Add the player's status (e.g., Active, Reserve/Injured)
                    })
    
    return roster_data

# Function to scrape coaches roster
def scrape_coaches_roster(coaches_url):
    response = requests.get(coaches_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    coaches_data = []

    # Find all featured coach sections
    featured_coach_sections = soup.find_all('div', class_='d3-o-person-card--featured')
    non_featured_coach_sections = soup.find_all('a', class_='d3-o-person-card--non-featured-coach')

    # Helper function to extract details from coach section
    def extract_coach_details(section, is_featured=False):
        try:
            # Coach name
            name = clean_text(section.find('h3', class_='d3-o-media-object__title').get_text(strip=True))

            # Coach title (position)
            title = clean_text(section.find('h5', class_='d3-o-media-object__roofline').get_text(strip=True))

            # Profile link
            profile_link_tag = section.find('a', class_='d3-o-media-object__link')
            profile_link = "No link" if not profile_link_tag else "https://www.steelers.com" + profile_link_tag.get('href')

            # Summary and experience extraction
            if is_featured:
                # For featured coaches, summary may be located in a div or p tag
                summary_div = section.find('div', class_='d3-o-media-object__summary')
                if summary_div:
                    summary = clean_text(summary_div.get_text(strip=True))
                else:
                    summary = "No summary available"
            else:
                # Non-featured coach summary and experience
                summary_tag = section.find('p', class_='d3-o-media-object__summary')
                experience_tag = summary_tag.find('strong') if summary_tag else None
                experience = experience_tag.get_text(strip=True) if experience_tag else "No experience available"
                summary = f"Experience: {experience}" if experience_tag else clean_text(summary_tag.get_text(strip=True)) if summary_tag else "No summary available"

            # Append coach data
            coaches_data.append({
                'name': name,
                'title': title,
                'summary': summary,
                'profile_link': profile_link
            })

        except AttributeError:
            # If any key attribute is missing, skip this coach entry
            pass

    # Extract details from featured coaches
    for section in featured_coach_sections:
        extract_coach_details(section, is_featured=True)

    # Extract details from non-featured coaches
    for section in non_featured_coach_sections:
        extract_coach_details(section, is_featured=False)

    return coaches_data


# Function to scrape front office roster
def scrape_front_office_roster(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    roster_data = []

    # Find all sections that have a title (h3) and the corresponding list (ul)
    sections = soup.find_all('div', class_='d3-o-person-card--table')
    
    for section in sections:
        try:
            # Get the section title (e.g., "Administration", "Coaching Staff")
            section_title = section.find('h3', class_='d3-o-box__title').get_text(strip=True)

            # Find the list of people in that section
            people = section.find_all('li')

            # Loop through each person and extract their name and role
            for person in people:
                name = clean_text_2(person.find('span', class_='d3-o-person-title').get_text(strip=True))
                role = clean_text_2(person.find('span', class_='d3-o-person-role').get_text(strip=True))
                
                # Add the data to the roster list
                roster_data.append({
                    'section': section_title,
                    'name': name,
                    'role': role
                })
        except AttributeError:
            # If any key attribute is missing, skip this entry
            continue

    return roster_data

# Function to scrape depth chart
def scrape_depth_chart(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    depth_chart = {}
    base_url = "https://www.steelers.com"  # Base URL for player profile links

    # Define strings for first, second, etc.
    strings = ["First", "Second", "Third", "Fourth", "Fifth"]

    # Find each table (Offense, Defense, Special Teams)
    depth_chart_sections = soup.find_all('table', class_='d3-o-depthchart')

    for table in depth_chart_sections:
        section = clean_text_2(table.find('caption').get_text())
        depth_chart[section] = []

        # Get position and players in each row
        rows = table.find('tbody').find_all('tr')

        for row in rows:
            position = clean_text_2(row.find('td').get_text())

            # Get the players for each depth (First, Second, etc.)
            players = []
            for i, player in enumerate(row.find_all('td', class_='d3-o-depthchart__tiers-5')):
                if player.a:
                    players.append({
                        'name': clean_text_2(player.a.get_text()),
                        'url': f"{base_url}{player.a['href']}",  # Prepend the base URL
                        'string': strings[i]  # Add string designation (First, Second, etc.)
                    })
                else:
                    players.append({'name': '', 'url': '', 'string': strings[i]})

            # Append the data for the position
            depth_chart[section].append({
                'position': position,
                'players': players
            })

    return depth_chart

# Combine all data into one JSON structure
def scrape_all_data():
    base_url = "https://www.steelers.com/team/"
    players_url = f"{base_url}players-roster/"
    coaches_url = f"{base_url}coaches-roster/"
    front_office_url = f"{base_url}front-office-roster/"
    depth_chart_url = f"{base_url}depth-chart/"
    
    data = {
        'players_roster': scrape_players_roster(players_url),
        'coaches_roster': scrape_coaches_roster(coaches_url),
        'front_office_roster': scrape_front_office_roster(front_office_url),
        'depth_chart': scrape_depth_chart(depth_chart_url),
    }

    with open('steelers_roster.json', 'w') as f:
        json.dump(data, f, indent=2)

    print("Data has been scraped and saved to steelers_roster.json")

# Execute the scraping process
scrape_all_data()
