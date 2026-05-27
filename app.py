from flask import Flask, render_template
import requests as http_requests
from steam_api import get_player_summary, get_owned_games, get_recently_played, get_achievements, get_game_schema

app = Flask(__name__)

@app.route("/")
def index():
    try:
        player = get_player_summary()
        recent = get_recently_played()
        if not recent:
            top_games = get_owned_games()[:5]
            section_title = "Most Played Games"
        else:
            top_games = recent
            section_title = "Recently Played"
    except http_requests.exceptions.RequestException:
        return render_template("error.html", message="Could not connect to Steam API. Try again later.")
    return render_template("index.html", player=player, games=top_games, section_title=section_title)

@app.route("/library")
def library():
    try:
        games = get_owned_games()
    except http_requests.exceptions.RequestException:
        return render_template("error.html", message="Could not load your game library.")
    return render_template("library.html", games=games)

@app.route("/stats")
def stats():
    try:
        games = get_owned_games()
    except http_requests.exceptions.RequestException:
        return render_template("error.html", message="Could not load stats.")
    total_hours = sum(g["playtime_forever"] for g in games) / 60
    played = [g for g in games if g["playtime_forever"] > 0]
    unplayed = len(games) - len(played)
    top10 = games[:10]
    chart_labels = [g["name"] for g in top10]
    chart_data = [round(g["playtime_forever"] / 60, 1) for g in top10]
    return render_template("stats.html",
        total_hours=round(total_hours, 1),
        total_games=len(games),
        played=len(played),
        unplayed=unplayed,
        chart_labels=chart_labels,
        chart_data=chart_data
    )

@app.route("/game/<int:app_id>")
def game(app_id):
    try:
        achievements = get_achievements(app_id)
        schema = get_game_schema(app_id)
    except http_requests.exceptions.RequestException:
        return render_template("error.html", message="Could not load achievements for this game.")
    if achievements is None:
        return render_template("game.html", app_id=app_id, achievements=None)
    merged = []
    for ach in achievements:
        name = ach["apiname"]
        info = schema.get(name, {})
        merged.append({
            "name": info.get("displayName", name),
            "description": info.get("description", ""),
            "icon": info.get("icon", ""),
            "icon_gray": info.get("icongray", ""),
            "achieved": ach["achieved"],
        })
    merged.sort(key=lambda a: a["achieved"], reverse=True)
    unlocked = sum(1 for a in merged if a["achieved"])
    return render_template("game.html", app_id=app_id, achievements=merged, unlocked=unlocked, total=len(merged))

if __name__ == "__main__":
    app.run(debug=True)