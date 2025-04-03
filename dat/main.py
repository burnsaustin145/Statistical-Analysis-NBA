import pickle
import pprint as pp
import csv


def write_csv(team, game_ids, dat, to_file, write, labels, stats_keys):
    write.writerow(labels)
    for id in game_ids:
        currRow = []
        currRow.append(id)
        teamPts = dat[id][team]['points']
        otherPts = dat[id]['home' if team == 'away' else 'away']['points']
        currRow.append(teamPts)
        currRow.append('win' if teamPts > otherPts else 'loss')
        try:
            currRow.append(dat[id]['attendance'])
        except:
            currRow.append("noinfo")
        for stat in stats_keys:
            currRow.append(dat[id]['home']['statistics'][stat])
        write.writerow(currRow)
    to_file.close()

def write_csv_with_location(game_ids, dat, to_file, write, labels, stats_keys, include_capacity=False):
    """Write CSV with home/away information and optionally venue capacity."""
    if "home_away" not in labels:
        labels.append("home_away")
    if include_capacity and "capacity" not in labels:
        labels.append("capacity")
    
    write.writerow(labels)
    
    for game_id in game_ids:
        print(game_id)
        if dat[game_id]['status'] != 'no_data':
            print("not no data")
            for location in ("home", "away"):
                curr_row = [game_id]
                team_pts = dat[game_id][location]['points']
                other_pts = dat[game_id]['home' if location == 'away' else 'away']['points']
                curr_row.append(team_pts)
                curr_row.append('win' if team_pts > other_pts else 'loss')
            try:
                curr_row.append(dat[game_id]['attendance'])
            except:
                curr_row.append("no_info")
            
            for stat in stats_keys:
                try:
                    curr_row.append(dat[game_id][location]['statistics'][stat])
                except:
                    curr_row.append("NA")
            
            curr_row.append(location)
            
            if include_capacity:
                try:
                    curr_row.append(dat[game_id]["venue"]["capacity"])
                except:
                    curr_row.append("NA")
            
            write.writerow(curr_row)

def generate_initial_labels(dat):
    game_ids = list(dat.keys())
    print("got ids")
    stats_keys = list(dat[game_ids[0]]['home']['statistics'])
    print(stats_keys)
    stats_keys.remove('most_unanswered')
    stats_keys.remove('periods')
    # from dat: id->home/away->points
    # id->home/away->statistics->{stats list all vars here}
    # id->attendance
    return stats_keys, game_ids

def generate_csv(stats_keys, game_ids, csv_name, include_capacity=True):
    """Generate CSV file with game data."""
    with open(csv_name, mode='w') as to_file:
        write = csv.writer(to_file, delimiter=',', quotechar='"')
        column_labels = ['Game Id', 'points', 'result', 'attendance']
        for lab in stats_keys:
            column_labels.append(lab)
        write_csv_with_location(game_ids, dat, to_file, write, column_labels, stats_keys, include_capacity)

def append_to_csv(game_id, dat, csv_name, stats_keys, include_capacity=True):
    """Append a single game's data to an existing CSV file."""
    import os
    file_exists = os.path.isfile(csv_name)
    
    with open(csv_name, mode='a') as to_file:
        write = csv.writer(to_file, delimiter=',', quotechar='"')
        
        # Write header if file doesn't exist
        if not file_exists:
            column_labels = ['Game Id', 'points', 'result', 'attendance']
            for lab in stats_keys:
                column_labels.append(lab)
            column_labels.append("home_away")
            if include_capacity:
                column_labels.append("capacity")
            write.writerow(column_labels)
        
        # Write data for both home and away
        for location in ("home", "away"):
            curr_row = [game_id]
            team_pts = dat[game_id][location]['points']
            other_pts = dat[game_id]['home' if location == 'away' else 'away']['points']
            curr_row.append(team_pts)
            curr_row.append('win' if team_pts > other_pts else 'loss')
            try:
                curr_row.append(dat[game_id]['attendance'])
            except:
                curr_row.append("no_info")
            
            for stat in stats_keys:
                try:
                    curr_row.append(dat[game_id][location]['statistics'][stat])
                except:
                    curr_row.append("NA")
            
            curr_row.append(location)
            
            if include_capacity:
                try:
                    curr_row.append(dat[game_id]["venue"]["capacity"])
                except:
                    curr_row.append("NA")
            
            write.writerow(curr_row)

def unpickle(jar_name):
    try:
        with open(jar_name, 'rb') as handle:
            dat = pickle.load(handle)
        print("got dat")
        return dat
    except:
        print("open pickle jar error")

# some initial testing
if __name__ == "__main__":
    # Load data
    dat = unpickle('pickledData10.pickle')
    keys, game_ids = generate_initial_labels(dat)
    print(game_ids)
    # Generate full CSV
    generate_csv(keys, game_ids, "tidy10_conf_true.csv")
    
    # Example of appending a single game (if it existed)
    # append_to_csv(game_ids[0], dat, "realtime_games.csv", keys)




