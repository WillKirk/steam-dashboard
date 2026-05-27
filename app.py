from flask import Flask, render_template
from steam_api import get_player_summary, get_owned_games

app = Flask(__name__)

@app.route("/")
def index():
    player = get_player_summary()
    return render_template("index.html", player=player)

@app.route("/library")
def library():
    games = get_owned_games()
    return render_template("library.html", games=games)

if __name__ == "__main__":
    app.run(debug=True)