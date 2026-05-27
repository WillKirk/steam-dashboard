from flask import Flask, render_template
from steam_api import get_player_summary, get_owned_games, get_recently_played

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

if __name__ == "__main__":
    app.run(debug=True)