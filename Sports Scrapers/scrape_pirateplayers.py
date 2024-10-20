import requests
from bs4 import BeautifulSoup
import json

# URLs for scraping
urls = {
    "roster": "https://www.mlb.com/pirates/roster",
    "depth_chart": "https://www.mlb.com/pirates/roster/depth-chart",
    "forty_man": "https://www.mlb.com/pirates/roster/40-man",
    "coaches": "https://www.mlb.com/pirates/roster/coaches"
}

def format_height(height):
    """Format height to remove spaces between feet and inches."""
    return height.replace(" ", "")

def get_player_data(url):
    """Scrape player data from a given MLB roster page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    players = []
    
    # Find player rows in the table
    for player_row in soup.select('tbody tr'):
        # Get player name
        name = player_row.select_one('.info a')
        # Get jersey number
        number = player_row.select_one('.jersey')
        # Get bat/throw info
        bat_throw = player_row.select_one('.bat-throw')
        # Get height, weight, and birthday
        height = player_row.select_one('.height')
        weight = player_row.select_one('.weight')
        birthday = player_row.select_one('.birthday')
        
        # Append the scraped data if name exists
        if name:
            player_data = {
                "name": name.get_text(strip=True),
                "number": number.get_text(strip=True) if number else "No Number",
                "bat_throw": bat_throw.get_text(strip=True) if bat_throw else "No B/T",
                "height": format_height(height.get_text(strip=True)) if height else "No Height",
                "weight": weight.get_text(strip=True) if weight else "No Weight",
                "birthday": birthday.get_text(strip=True) if birthday else "No DOB"
            }
            players.append(player_data)
    
    return players

def get_coaches_data(url):
    """Scrape coach data from the coaching staff page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    coaches = []
    
    # Find coach rows in the table
    for coach_row in soup.select('tbody tr'):
        # Get coach name
        name = coach_row.select_one('.info')
        # Get coach jersey number
        number = coach_row.select_one('.jersey')
        # Get coach position
        position = coach_row.select_one('.position')
        
        # Append the scraped data if name exists
        if name:
            coach_data = {
                "name": name.get_text(strip=True),
                "number": number.get_text(strip=True) if number else "No Number",
                "position": position.get_text(strip=True) if position else "No Position"
            }
            coaches.append(coach_data)
    
    return coaches

def main():
    roster_data = {}
    
    # Scrape player data from different pages
    roster_data['roster'] = get_player_data(urls['roster'])
    roster_data['depth_chart'] = get_player_data(urls['depth_chart'])
    roster_data['forty_man'] = get_player_data(urls['forty_man'])
    
    # Scrape coach data
    roster_data['coaches'] = get_coaches_data(urls['coaches'])
        
    # Write data to a JSON file
    with open('pirates_roster.json', 'w') as json_file:
        json.dump(roster_data, json_file, indent=4)
    
    print("Roster data successfully written to pirates_roster_data.json")

if __name__ == "__main__":
    main()
