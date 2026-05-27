from flask import Flask, render_template
from steam_api import get_player_summary

app = Flask(__name__)

@app.route("/")
def index():
    player = get_player_summary()
    return render_template("index.html", player=player)

if __name__ == "__main__":
    app.run(debug=True)