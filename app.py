import os
import sys

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload

from util import generate_games_resp, server_game_to_client

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_RECORD_QUERIES"] = True
db = SQLAlchemy(app)

from models import Game, Round, User

@app.route("/games/<user_id>", methods=["GET"])
def games(user_id):
    user = User.query.options(
        joinedload(User.games).joinedload(Game.players),
        joinedload(User.games).joinedload(Game.rounds)).get(user_id)

    return jsonify(generate_games_resp(user, user.games))

@app.route("/update-user", methods=["POST"])
def update_user():
    params = request.get_json()
    user_id = params["id"]
    name = params["name"]
    first_name = params["firstName"]
    last_name = params["lastName"]
    fb_token = params["fbToken"]

    user = User.query.get(user_id)
    if user:
        user.name = name
        user.first_name = first_name
        user.last_name = last_name
        user.fb_token = fb_token
    else:
        user = User(user_id, name, first_name, last_name, fb_token)

    db.session.add(user)
    db.session.commit()

    return "ok"

@app.route("/create-game", methods=["POST"])
def create_game():
    params = request.get_json()
    player1_id = params["player1Id"]
    player2_id = params["player2Id"]

    players = User.query.filter(User.id.in_([player1_id, player2_id]))
    assert players.count() == 2
    game = Game(player1_id)
    request_user = None
    for player in players:
        game.players.append(player)
        if player.id == player1_id:
            request_user = player
    game.rounds.append(Round("WORD", player1_id))

    db.session.add(game)
    db.session.commit()

    return jsonify(server_game_to_client(request_user, game))

@app.route("/update-round", methods=["POST"])
def update_round():
    params = request.get_json()
    round_id = params["id"]
    clues = params["clues"]
    guesses = params["guesses"]
    replayed = params["replayed"]

    round = Round.query.get(round_id)
    assert round
    round.clues = clues
    round.guesses = guesses
    round.replayed = replayed

    db.session.add(round)
    db.session.commit()

    return "ok"
