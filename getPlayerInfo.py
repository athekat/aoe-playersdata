import json
import requests
import datetime

# Define player information dictionary
players = {}
today = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

# Define API endpoints for each player
player_urls = {
    "dicopato": "https://aoe-api.worldsedgelink.com/community/leaderboard/GetPersonalStat?title=age2&profile_names=[%22/steam/76561198118459931%22]",
    "dicopatito": "https://aoe-api.worldsedgelink.com/community/leaderboard/GetPersonalStat?title=age2&profile_names=[%22/steam/76561199195740571%22]",
    "pato350z": "https://aoe-api.worldsedgelink.com/community/leaderboard/GetPersonalStat?title=age2&profile_names=[%22/steam/76561198774258334%22]",
    "sir_monkey": "https://aoe-api.worldsedgelink.com/community/leaderboard/GetPersonalStat?title=age2&profile_names=[%22/steam/76561198163778606%22]",
    "nanox": "https://aoe-api.worldsedgelink.com/community/leaderboard/GetPersonalStat?title=age2&profile_names=[%22/steam/76561198191637438%22]",
    "alanthekat": "https://aoe-api.worldsedgelink.com/community/leaderboard/GetPersonalStat?title=age2&profile_names=[%22/steam/76561198153797281%22]",
    "carpincho": "https://aoe-api.worldsedgelink.com/community/leaderboard/GetPersonalStat?title=age2&profile_names=[%22/steam/76561199207580572%22]",
    "emo": "https://aoe-api.worldsedgelink.com/community/leaderboard/GetPersonalStat?title=age2&profile_names=[%22/steam/76561198399299731%22]",
    "thexcarpincho": "https://aoe-api.worldsedgelink.com/community/leaderboard/GetPersonalStat?title=age2&profile_names=[%22/xboxlive/F7577FE856E4AEDA15094BF4CEA3610BA6403A5D%22]",
}

def get_player_stats(url):
  """Fetches player stats from the provided API URL.

  Args:
      url: The API endpoint URL.

  Returns:
      A dictionary containing extracted player stats (win, losses, rating, lastmatchdate)
      for each leaderboard.
  """
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for non-2xx status codes

    data = response.json()
    leaderboard_stats = data.get("leaderboardStats", [])

    # Filter leaderboard stats for Leaderboard 3 and 4
    relevant_stats = [
        stat
        for stat in leaderboard_stats
        if stat["leaderboard_id"] in (3, 4)
    ]

    # Extract desired information and store in separate dictionaries
    player_data = {}
    for stat in relevant_stats:
        leaderboard_id = stat["leaderboard_id"]
    
        player_data.setdefault(leaderboard_id, {})  
        player_data[leaderboard_id].update({
            "win": stat["wins"],
            "losses": stat["losses"],
            "rating": stat["rating"],
            "lastmatchdate": datetime.datetime.fromtimestamp(stat['lastmatchdate']).strftime('%d/%m/%Y'),
    })
    return player_data

  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from {url}: {e}")
    return None


# Loop through players and collect stats
for player_name, url in player_urls.items():
  player_stats = get_player_stats(url)
  if player_stats:
    players[player_name] = player_stats
    

# Write player data to JSON file with today's date
with open("player_stats.json", "w") as outfile:
  json.dump(players, outfile, indent=4)

with open("lastUpdated.txt", "w") as outfile:
    outfile.write(today)

print("Player stats successfully written to player_stats.json")
