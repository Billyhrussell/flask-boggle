from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

from wordlist import english_words

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4()) #creates a new string game_id
    game = BoggleGame() #creates a new game instance
    games[game_id] = game #adds game value to game_id key in games dict

    return jsonify({"gameId": game_id, "board": game.board})
    # games.gameId = game_id
    # games.board = game
    # game.board = list of lists (list with 5 lists of 5 letters)

@app.post("/api/score-word")
def score_word():
    """Accepts a JSON {game_id, word} and checks if the word is legal:
    1. word is on the word list
    2. word is on the board
    Returns a JSON response using jsonify """

    game_id = request.json.get("game_id")
    word = request.json.get("word")
    game = games[game_id]

    if not game.is_word_in_word_list(word):
        return jsonify(result = "not-word")
    if not game.check_word_on_board(word):
        return jsonify(result = "not-on-board")
    else:
        return jsonify(result= "ok")