import json
from flask import Blueprint, request
from app import pusher

auth = Blueprint("auth", __name__)
@auth.route("/pusher/auth", methods=["POST"])
def auth_pusher():
    auth = pusher.authenticate(
        channel = request.form["channel_name"],
        socket_id = request.form["socket_id"] 
    )
    return json.dumps(auth)