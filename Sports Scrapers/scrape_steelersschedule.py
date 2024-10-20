import requests
from bs4 import BeautifulSoup
import json

# Function to clean and strip text
def clean_text(text):
    return ' '.join(text.split()).replace('\xa0', ' ')

def clean_escape_sequences(data):
    cleaned_data = []
    for game in data:
        cleaned_game = {}
        for key, value in game.items():
            if isinstance(value, str):
                # Remove the escape sequences and clean the strings
                cleaned_game[key] = value.replace('\u00b7', '').strip()
            else:
                cleaned_game[key] = value
        cleaned_data.append(cleaned_game)
    return cleaned_data

# Function to check if a game is a preseason game
def is_preseason_game(date):
    # Preseason games are typically played in August
    return '08/' in date

def scrape_steelers_schedule(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    games = []

    # Find all game cards for both completed and future games
    game_cards = soup.find_all('div', class_='nfl-o-matchup-cards')

    for game in game_cards:
        try:
            game_type = game['class'][1] if len(game['class']) > 1 else None

            # Extract game week
            week = game.find('strong').get_text(strip=True)

            # Extract date and time
            date_info = game.find_all('span')
            date = clean_text(date_info[0].get_text()) if len(date_info) > 0 else "TBD"
            time = clean_text(date_info[1].get_text()) if len(date_info) > 1 else "TBD"

            # Extract opponent
            opponent_name = game.find('p', class_='nfl-o-matchup-cards__team-full-name').get_text(strip=True)

            # Extract venue
            venue = game.find('span', class_='nfl-o-matchup-cards__venue--location').get_text(strip=True)

            # Determine if it's a preseason game
            preseason = is_preseason_game(week)

            # Initialize placeholders
            result = "TBD"
            score = "TBD"

            if game_type == 'nfl-o-matchup-cards--post-game':
                # Extract result and score for completed games
                result = game.find('span', class_='nfl-o-matchup-cards__score--result').get_text(strip=True)
                score = game.find('span', class_='nfl-o-matchup-cards__score--points').get_text(strip=True)

            # Add game data to list
            games.append({
                'week': week,
                'date': date,
                'time': time,
                'opponent': opponent_name,
                'result': result,
                'score': score,
                'venue': venue,
                'preseason': preseason
            })

        except AttributeError as e:
            print(f"Skipping an entry due to missing data: {e}")
            continue

    return games


# Function to save games to a JSON file
def save_schedule_to_json(games, file_name='steelers_schedule.json'):
    with open(file_name, 'w') as file:
        json.dump(games, file, indent=2)
    print(f"Schedule saved to {file_name}")

# Scrape and save the schedule to a JSON file
schedule_url = 'https://www.steelers.com/schedule/'
steelers_schedule = scrape_steelers_schedule(schedule_url)
cleaned_schedule = clean_escape_sequences(steelers_schedule)
save_schedule_to_json(cleaned_schedule)