import requests
import json

def fetch_and_save_player_data(players):
  """Fetches match data for multiple players and saves it to a JSON file.

  Args:
      players (list): A list of dictionaries containing player name and API URL.
  """

  player_data = {}
  for player in players:
      player_name = player['name']
      api_url = player['api_url']

      try:
          response = requests.get(api_url)
          response.raise_for_status()  # Raise an exception for error HTTP statuses
          data = response.json()

          if data['matches']:
              last_match = data['matches'][0]
              teams = {}
              for team in last_match['teams']:
                  team_id = team['teamId']
                  teams[f"Team {team_id}"] = []
                  for player in team['players']:
                      player_name_in_match = player['name']
                      civ_name = player['civName']
                      elo = player['rating']
                      outcome = player['won']
                      profileId = player['profileId']
                      if outcome:
                          outcome = "&#128081;"  # Victory emoji
                      elif outcome is False:
                          outcome = "&#128128;"  # Defeat emoji
                      else:
                          outcome = "&#128355"
                      teams[f"Team {team_id}"].append(f"{player_name_in_match} ({elo}) - {civ_name} {outcome}")

            # Join the team members with newline characters, without extra commas
              for team_id in teams:
                  teams[team_id] = "<br>".join(teams[team_id])

              final_json = {
                  player_name: {
                      "LastMatch": f"<img src='{last_match['mapImageUrl']}' width='150rem' alt=''>",
                      "DownloadRecLink": f"<a class='align-self-center link-light link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover' href='https://aoe.ms/replay/?gameId={last_match['matchId']}&profileId={profileId}'>Download &#128190;</a>",  # Download replay link
                      **teams
                  }
              }
              player_data.update(final_json)

          else: 
              print(f"No recent matches found for player: {player_name}")

      except requests.exceptions.RequestException as e:
          print(f"Error fetching data for player {player_name}: {e}")

  # Save the player data to a JSON file
  if player_data:  # Check if any player data was collected
      with open('mostrecentmatch.json', 'w') as f:
          json.dump(player_data, f, indent=4)
      print("Player match data saved to player_matches.json")

# Replace with your list of players in dictionary format
players = [
    {"name": "Carpincho", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=6446904&search=&page=1"},
    {"name": "Dicopatito", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=6237950&search=&page=1"},
    {"name": "Nanox", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=439001&search=&page=1"},
    {"name": "SirMonkey", "api_url": "https://data.aoe2companion.com/api/matches?profile_ids=903496&search=&page=1"}
]

fetch_and_save_player_data(players)
