from flask_socketio import emit
from __main__ import socketio, clients

@socketio.on("connect")
def connection():
    emit("Hello!", {"data": "y u reading dis"})
    print("User connected!")

@socketio.on("disconnect")
def disconnect():
    print("User disconnected!")

@socketio.on("create-player")
def create_player(data):
    """Create a player and store them in the client object"""
    try:
        success = clients.create_player(data["clientId"], data["username"])

        if not success:
            emit("error", {"message": "player was not added"})
    except Exception as _:
        emit("error", {"message": "user data was not provided"})