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

def get_achievements(app_id):
    url = f"{BASE_URL}/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": STEAM_ID,
        "appid": app_id
    }
    response = requests.get(url, params=params)
    if response.status_code == 403:
        return None  # Game doesn't support achievements
    response.raise_for_status()
    data = response.json()["playerstats"]
    if not data.get("success") or "achievements" not in data:
        return None
    return data["achievements"]

def get_game_schema(app_id):
    url = f"{BASE_URL}/ISteamUserStats/GetSchemaForGame/v2/"
    params = {
        "key": STEAM_API_KEY,
        "appid": app_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    stats = response.json().get("game", {}).get("availableGameStats", {})
    achievements = stats.get("achievements", [])
    # Return as a dict keyed by achievement name for easy lookup
    return {a["name"]: a for a in achievements}