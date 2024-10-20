import requests
import json

# Function to fetch and process schedule data for a specific month
def fetch_schedule(start_date, end_date, team_id):
    url = f"https://statsapi.mlb.com/api/v1/schedule?lang=en&sportIds=1,51,21&hydrate=team(venue(timezone)),venue(timezone),game(seriesStatus,seriesSummary,tickets,promotions,sponsorships,content(summary,media(epg))),seriesStatus,seriesSummary,broadcasts(all),linescore,tickets,event(tickets,game,sport,league,status,xref),radioBroadcasts&season=2025&startDate={start_date}&endDate={end_date}&teamId={team_id}&timeZone=America/New_York&eventTypes=primary&scheduleTypes=games,events,xref"
    
    # Make the GET request to fetch the schedule
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        schedule_data = response.json()
        
        # Initialize list to hold game details
        game_details = []

        # Iterate over each date and game
        for date_obj in schedule_data.get("dates", []):
            for game in date_obj.get("games", []):
                game_info = {
                    "date": game["officialDate"],
                    "opponent": game["teams"]["away"]["team"]["name"] if game["teams"]["away"]["team"]["id"] != team_id else game["teams"]["home"]["team"]["name"],
                    "home_away": "Away" if game["teams"]["away"]["team"]["id"] == team_id else "Home",
                    "status": game["status"]["detailedState"]
                }
                game_details.append(game_info)

        return game_details
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")
        return []

# Function to fetch schedules for each month and save them in a JSON file
def fetch_and_save_schedule():
    # List of months with their start and end dates
    months = [
        ("2025-02-01", "2025-02-28"),
        ("2025-03-01", "2025-03-31"),
        ("2025-04-01", "2025-04-30"),
        ("2025-05-01", "2025-05-31"),
        ("2025-06-01", "2025-06-30"),
        ("2025-07-01", "2025-07-31"),
        ("2025-08-01", "2025-08-31"),
        ("2025-09-01", "2025-09-30")
    ]
    
    # Pittsburgh Pirates team ID
    team_id = 134
    
    # Initialize a list to hold all game details
    all_games = []
    
    # Fetch and accumulate schedule data for each month
    for start_date, end_date in months:
        monthly_games = fetch_schedule(start_date, end_date, team_id)
        all_games.extend(monthly_games)
    
    # Save the combined data to a JSON file
    with open('pirates_schedule.json', 'w') as f:
        json.dump(all_games, f, indent=2)
    
    print("Schedule saved to pirates_schedule.json")

# Call the function to fetch and save the schedule
fetch_and_save_schedule()
