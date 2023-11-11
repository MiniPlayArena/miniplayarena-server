from flask_socketio import emit, join_room, leave_room
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

        if success:
            emit("player-created", {"clientId": data["clientId"]})
        else:
            emit("error", {"message": "player was not added, likely already created or username is too short"})
    except Exception as _:
        emit("error", {"message": "user data was not provided"})

@socketio.on("create-party")
def create_party(data):
    """Create a player and store them in the client object"""
    try:
        success, party_id = clients.create_party(data["partyLeader"])

        if success:
            join_room(party_id)
            emit("party-created", {"partyId": party_id, "partyLeader": data["partyLeader"]})
        else:
            emit("error", {"message": "party was not created"})
    except Exception as _:
        emit("error", {"message": "user data was not provided"})


@socketio.on("join-party")
def join_party(data):
    """Attempt to join a party"""
    try:
        success = clients.join_party(data["partyId"], data["clientId"])

        if success:
            join_room(data["partyId"])
            emit("joined-party", {"partyId": data["partyId"], "clientId": data["clientId"]})
        else:
            emit("error", {"message": "player could not join party, either it didn't exist or they are in a party already"})
    except Exception as _:
        emit("error", {"message": "user data was not provided"})