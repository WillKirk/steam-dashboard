from flask import Flask, render_template
from steam_api import get_player_summary, get_owned_games, get_recently_played, get_achievements, get_game_schema

app = Flask(__name__)

@app.route("/")
def index():
    player = get_player_summary()
    recent = get_recently_played()
    
    if not recent:
        top_games = get_owned_games()[:5]
        section_title = "Most Played Games"
    else:
        top_games = recent
        section_title = "Recently Played"
    
    return render_template("index.html", player=player, games=top_games, section_title=section_title)

@app.route("/library")
def library():
    games = get_owned_games()
    return render_template("library.html", games=games)

@app.route("/game/<int:app_id>")
def game(app_id):
    achievements = get_achievements(app_id)
    schema = get_game_schema(app_id)
    
    if achievements is None:
        return render_template("game.html", app_id=app_id, achievements=None)
    
    # Merge achievement status with schema (for display names and icons)
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
    
    # Sort — unlocked first, then locked
    merged.sort(key=lambda a: a["achieved"], reverse=True)
    
    unlocked = sum(1 for a in merged if a["achieved"])
    
    return render_template("game.html", app_id=app_id, achievements=merged, unlocked=unlocked, total=len(merged))

if __name__ == "__main__":
    app.run(debug=True)