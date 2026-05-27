import requests
from config import STEAM_API_KEY, STEAM_ID

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

def get_owned_games():
    url = f"{BASE_URL}/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": STEAM_ID,
        "include_appinfo": True,
        "include_played_free_games": True
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    games = response.json()["response"].get("games", [])
    # Sort by playtime, most played first
    return sorted(games, key=lambda g: g["playtime_forever"], reverse=True)

def get_recently_played():
    url = f"{BASE_URL}/IPlayerService/GetRecentlyPlayedGames/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": STEAM_ID,
        "count": 5
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["response"].get("games", [])