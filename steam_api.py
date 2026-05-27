import requests
from config import STEAM_API_KEY, STEAM_ID

print(f"KEY: '{STEAM_API_KEY}'")
print(f"ID: '{STEAM_ID}'")

BASE_URL = "https://api.steampowered.com"

def get_player_summary():
    url = f"{BASE_URL}/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": STEAM_API_KEY,
        "steamids": STEAM_ID
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    players = response.json()["response"]["players"]
    return players[0] if players else None