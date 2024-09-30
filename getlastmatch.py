import requests
import json

# Player
players = {
    "Dicopatito": "https://data.aoe2companion.com/api/nightbot/match?steam_id=76561199195740571&color=false&flag=true",
    "Pato": "https://data.aoe2companion.com/api/nightbot/match?steam_id=76561198118459931&color=false&flag=true",
    "Nanox": "https://data.aoe2companion.com/api/nightbot/match?steam_id=76561198191637438&color=false&flag=true",
    "Sir Monkey": "https://data.aoe2companion.com/api/nightbot/match?steam_id=76561198163778606&color=false&flag=true",
    "alanthekat": "https://data.aoe2companion.com/api/nightbot/match?steam_id=76561198153797281&color=false&flag=true",
    "Carpincho": "https://data.aoe2companion.com/api/nightbot/match?steam_id=76561199207580572&color=false&flag=true",
    "thexcarpincho": "https://data.aoe2companion.com/api/nightbot/match?profile_id=18660623&color=false&flag=true",
}

def get_match_info(player_name, api_url):
    try:
        response = requests.get(api_url)
        data = response.json()
        print(f"API response for {player_name}:\n{data}")
        text = data

        # Remove "playing" word using regular expression (more robust)
        import re
        processed_text = re.sub(r" playing ", " ", text)

        return {player_name: processed_text}
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data for {player_name}: {e}")
        return {player_name: "Error"}  # Indicate error in the JSON

# Collect data for all players
all_data = []
for player_name, api_url in players.items():
    data = get_match_info(player_name, api_url)
    all_data.append(data)

# Save data to JSON file
with open("mostrecentmatch.json", "w") as f:
    json.dump(all_data, f, indent=4)  # Pretty-print JSON for readability

print("Match data saved to mostrecentmatch.json")