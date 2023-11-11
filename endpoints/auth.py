from flask import Blueprint

new_game = Blueprint("auth", __name__)
@new_game.route("/pusher/new_game", methods=["POST"])
def authenticate_new_game():
    return "guh"