import json
import requests
from datetime import datetime

# Convert timestamp to date
def convert_timestamp_to_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d, %H:%M:%S')

# Civ Mapping (might change with new civs DLC)
civ_list = {
    1: "Aztecs", 2: "Bengalis", 3: "Berbers", 4: "Bohemians", 5: "Britons",
    6: "Bulgarians", 7: "Burgundians", 8: "Burmese", 9: "Byzantines", 10: "Celts",
    11: "Chinese", 12: "Cumans", 13: "Dravidians", 14: "Ethiopians", 15: "Franks",
    17: "Goths", 18: "Gurjaras", 19: "Huns", 20: "Incas", 21: "Hindustanis", 22: "Italians",
    23: "Japanese", 24: "Khmer", 25: "Koreans", 26: "Lithuanians", 27: "Magyars",
    28: "Malay", 29: "Malians", 30: "Mayans", 31: "Mongols", 32: "Persians",
    33: "Poles", 34: "Portuguese", 36: "Saracens", 37: "Sicilians", 38: "Slavs",
    39: "Spanish", 40: "Tatars", 41: "Teutons", 42: "Turks", 43: "Vietnamese",
    44: "Vikings", 35: "Romans", 0: "Armenians", 16: "Georgians"
}

# Player IDs with desired names as keys
player_ids = {
    "Carpincho": "76561199207580572",
    "Dicopatito": "76561199195740571",
    "SirMonkey": "76561198163778606",
    "Nanox": "76561198191637438"
}

# Main dictionary to hold data for each player
all_player_data = {}

# Loop through each player name and ID in the dictionary
for player_name, player_id in player_ids.items():
    # API URL for each player using the correct player_id
    URL = f"https://aoe-api.worldsedgelink.com/community/leaderboard/getRecentMatchHistory?title=age2&profile_names=[%22/steam/{player_id}%22]"
    
    try:
        # Make the request
        response = requests.get(URL, timeout=10)
        player_data = response.json()

        # Check if 'matchHistoryStats' key is present
        if 'matchHistoryStats' not in player_data:
            print(f"No 'matchHistoryStats' key found for {player_name}. Skipping...")
            continue
        
        matches = player_data['matchHistoryStats']
        profiles = player_data.get('profiles', [])
        
        # Map profile_id to alias
        profile_id_to_alias = {profile['profile_id']: profile['alias'] for profile in profiles}

        # Find the most recent match
        most_recent_match = max(matches, key=lambda x: x.get('startgametime', 0))
        match_date = convert_timestamp_to_date(most_recent_match.get('startgametime', 0))

        # Team info
        grouped_by_team = {}
        for member in most_recent_match.get('matchhistorymember', []):
            matchhistory_id=member['matchhistory_id']
            profile_id = member['profile_id']
            outcome = member['outcome']
            civ_name = civ_list.get(member.get('civilization_id', -1), "Unknown")
            alias = profile_id_to_alias.get(member.get('profile_id'), "Unknown Alias")
            elo = member.get('oldrating', "Unknown")
            team_id = member.get('teamid', -1)
            if outcome == 1:
                outcome = "&#128081;"
            else:
                outcome = "&#128128;"            
            player_info = f"{alias} ({elo}) - {civ_name} {outcome}"
            if team_id not in grouped_by_team:
                grouped_by_team[team_id] = []
            grouped_by_team[team_id].append(player_info)

        # Format team information
        teams_output = {}
        for team_id, players in grouped_by_team.items():
            teams_output[f"Team {team_id + 1}"] = "<br>".join(players)

        # Store data using player_name as key
        all_player_data[player_name] = {
            "LastMatch": f"<b>Last Match</b><br>Map: {most_recent_match.get('mapname', 'Unknown')}<br>",
            **teams_output,
            "DownloadRecLink": f"<a class='align-self-center link-light link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover' href='https://aoe.ms/replay/?gameId={matchhistory_id}&profileId={profile_id}'>Download Rec</a>"
        }

    except requests.RequestException as e:
        print(f"Request failed for {player_name}: {e}")
    except KeyError as e:
        print(f"Key error for {player_name}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {player_name}: {e}")

# Write the data to a JSON file
with open("mostrecentmatch.json", "w") as outfile:
    json.dump(all_player_data, outfile, indent=4)
