import requests
import pickle
import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Hide API key in environment variable or config file (recommended approach)    
load_dotenv('.env')
API_KEY = os.getenv("NBA_API_KEY")  # Default for testing only
print(API_KEY)
def fetch_game_schedule_by_phase(season_year: str, season_phase: str, api_key: str) -> Dict:
    """Fetch the game schedule for a given season and phase."""
    url = f"https://api.sportradar.us/nba/trial/v8/en/games/{season_year}/{season_phase}/schedule.json?api_key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching schedule: {e}")
        return {}
    
def fetch_game_schedule_by_day(season_year: str, month: str, day: str, api_key: str) -> Dict:
    """Fetch the game schedule for a given season and phase."""
    url = f"https://api.sportradar.us/nba/trial/v8/en/games/{season_year}/{month}/{day}/schedule.json?api_key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching schedule: {e}")
        return {}

def fetch_boxscore(game_id: str, api_key: str) -> Optional[Dict]:
    """Fetch the boxscore summary for a specific game."""
    url = f"https://api.sportradar.us/nba/trial/v8/en/games/{game_id}/summary.json?api_key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching boxscore for game {game_id}: {e}")
        return None

def collect_realtime_data(season_year: str, month: str, day: str, max_calls: int = 50, output_file: str = "realtime_data.pickle") -> None:
    """Collect real-time NBA game data and save it to a pickle file."""
    all_data = {}
    game_count = 0

    # Fetch the schedule
    schedule_data = fetch_game_schedule_by_day(season_year, month, day, API_KEY)
    if not schedule_data or "games" not in schedule_data:
        print("No games found in schedule.")
        return

    # Process each game
    for game in schedule_data["games"]:
        if game_count >= max_calls:
            break
        
        game_id = game["id"]
        boxscore_data = fetch_boxscore(game_id, API_KEY)
        
        if boxscore_data:
            all_data[game_id] = boxscore_data
        else:
            all_data[game_id] = {"status": "no_data"}
        
        game_count += 1

    # Save to pickle file
    try:
        with open(output_file, 'wb') as handle:
            pickle.dump(all_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"Data saved to {output_file}")
    except Exception as e:
        print(f"Failed to save data to {output_file}: {e}")

if __name__ == "__main__":
    # Example usage for real-time data collection
    collect_realtime_data(season_year="2024", month="12", day="25", max_calls=10, output_file="pickledData10.pickle")