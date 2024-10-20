import requests
import json

team_name_dict = {
    "NA": "Anaheim Ducks",
    "BOS": "Boston Bruins",
    "BUF": "Buffalo Sabres",
    "CAR": "Carolina Hurricanes",
    "CBJ": "Columbus Blue Jackets",
    "CGY": "Calgary Flames",
    "CHI": "Chicago Blackhawks",
    "COL": "Colorado Avalanche",
    "DAL": "Dallas Stars",
    "DET": "Detroit Red Wings",
    "EDM": "Edmonton Oilers",
    "FLA": "Florida Panthers",
    "LAK": "Los Angeles Kings",
    "MIN": "Minnesota Wild",
    "MTL": "Montreal Canadiens",
    "NJD": "New Jersey Devils",
    "NSH": "Nashville Predators",
    "NYI": "New York Islanders",
    "NYR": "New York Rangers",
    "OTT": "Ottawa Senators",
    "PHI": "Philadelphia Flyers",
    "PIT": "Pittsburgh Penguins",
    "SEA": "Seattle Kraken",
    "SJS": "San Jose Sharks",
    "STL": "St. Louis Blues",
    "TBL": "Tampa Bay Lightning",
    "TOR": "Toronto Maple Leafs",
    "UTA": "Utah Hockey Club",
    "VAN": "Vancouver Canucks",
    "VGK": "Vegas Golden Knights",
    "WPG": "Winnipeg Jets",
    "WSH": "Washington Capitals"
}

# Function to replace special characters like \u00e9 with normal 'e'
def clean_text(text):
    return text.replace('\u00e9', 'e')

# Function to determine if the Penguins are home or away
def get_home_away(game, penguins_id=5):
    if game['homeTeam']['id'] == penguins_id:
        return 'home', game['awayTeam']
    else:
        return 'away', game['homeTeam']

# Function to determine the winner (handle games without a final score)
def get_winner(game, penguins_id=5):
    if 'score' not in game['homeTeam'] or 'score' not in game['awayTeam']:
        return "TBD"  # For games that haven't happened yet
    if game['homeTeam']['score'] > game['awayTeam']['score']:
        winner_id = game['homeTeam']['id']
    else:
        winner_id = game['awayTeam']['id']

    if winner_id == penguins_id:
        return "Penguins"
    else:
        return "Opponent"

# Function to format the game data
def format_game_data(game):
    home_away, opponent_team = get_home_away(game)
    winner = get_winner(game)

    # Handle missing score for future games
    if 'score' in game['homeTeam'] and 'score' in game['awayTeam']:
        score = f"{game['homeTeam']['score']} - {game['awayTeam']['score']}"
    else:
        score = "TBD"

    opponent_abbrev = opponent_team['abbrev']
    opponent_name = team_name_dict.get(opponent_abbrev, "Unknown Team")

    return {
        'game_date': game['gameDate'],
        'venue': game['venue']['default'],
        'home_away': home_away,
        'opponent': opponent_name,
        'winner': winner,
        'score': score
    }

# Fetching the game data for the 2024-2025 season
url = 'https://api-web.nhle.com/v1/club-schedule-season/pit/20242025'
response = requests.get(url)
games_data = response.json()['games']

# Extracting and formatting the relevant data
penguins_games = [format_game_data(game) for game in games_data]

# Saving the extracted data to a JSON file
with open('penguins_schedule.json', 'w') as json_file:
    json.dump(penguins_games, json_file, indent=4)

print("Schedule saved to penguins_schedule.json")
