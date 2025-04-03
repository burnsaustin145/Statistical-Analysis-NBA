# dat/simulate_realtime_to_csv.py
# Simulate fetching real-time NBA data and overwrite a CSV file with game details.

import csv
import os
import time

import numpy as np

from datetime import datetime
from typing import Dict
from apiCall import fetch_game_schedule_by_day, fetch_boxscore, API_KEY
from main import generate_initial_labels, generate_csv, write_to_csv



def simulate_realtime_to_csv(season_year: str, month: str, day: str, output_file: str = "realtime_data.csv") -> None:
    """Simulate fetching real-time NBA data and overwrite it to a CSV file.

    Args:
        season_year (str): The season year (e.g., '2024').
        month (str): The month (e.g., '12').
        day (str): The day (e.g., '25').
        output_file (str): The CSV file to overwrite (default: 'realtime_data.csv').

    Returns:
        the current real time file name 
    """
    # Fetch the daily schedule
    schedule_data: Dict = fetch_game_schedule_by_day(season_year, month, day, API_KEY)
    if not schedule_data or "games" not in schedule_data:
        print("No games found in schedule.")
        return
    if schedule_data["games"] != []:
            game_id = schedule_data["games"][0]["id"]
            boxscore_data = fetch_boxscore(game_id, API_KEY)

            print(boxscore_data)
            all_data = {}
            # Prepare row data
            if boxscore_data:
                all_data[game_id] = boxscore_data
            else:
                 print("no data")
                 return 
    curr_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    keys, game_ids = generate_initial_labels(all_data)
    print(game_ids)
    if not os.path.exists(f"realtime_games_{curr_datetime}.csv"):
        generate_csv(keys, game_ids, f"realtime_games_{curr_datetime}.csv", all_data)

    # Open CSV file in write mode (overwrites existing file)
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['game_id', 'status', 'home_team', 'away_team', 'scheduled_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # write data to csv slowly over time
        max_home_score = all_data[game_id]['home']['points']
        max_away_score = all_data[game_id]['away']['points']
        print(max_home_score)
        home_score_steps = np.linspace(0, max_home_score, 100, dtype=int)
        away_score_steps = np.linspace(0, max_away_score, 100, dtype=int)
        for home_score, away_score in zip(home_score_steps, away_score_steps):
            time.sleep(10)
            all_data[game_id]['home']['points'] = home_score
            all_data[game_id]['away']['points'] = away_score
            print("updated data")
            print(all_data[game_id]['home']['points'])
            print(all_data[game_id]['away']['points'])
            write_to_csv(game_id, all_data, f"realtime_games_{curr_datetime}.csv", keys)

        return f"realtime_games_{curr_datetime}.csv"

if __name__ == "__main__":
    # Simulate fetching data for a specific date
    simulate_realtime_to_csv(season_year="2024", month="11", day="25", output_file="realtime_data.csv") 