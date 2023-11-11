from flask_socketio import emit, join_room, leave_room, send
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
            emit(
                "error",
                {
                    "message": "player was not added, likely already created or username is too short"
                },
            )
    except Exception as e:
        emit("error", {"message": e})


@socketio.on("create-party")
def create_party(data):
    """Create a player and store them in the client object"""
    try:
        success, party_id, party = clients.create_party(data["partyLeader"])
        party_leader = party[0]

        if success:
            join_room(party_id)
            emit(
                "party-created",
                {
                    "partyId": party_id,
                    "partyLeader": party_leader,
                    "players": party,
                },
            )
        else:
            emit("error", {"message": "party was not created"})
    except Exception as e:
        emit("error", {"message": e})


@socketio.on("join-party")
def join_party(data):
    """Attempt to join a party"""
    try:
        success, party = clients.join_party(data["partyId"], data["clientId"])
        party_leader = party[0]

        if success: 
            join_room(data["partyId"])
            emit(
                "joined-party",
                {
                    "partyId": data["partyId"],
                    "clientId": data["clientId"],
                    "partyLeader": party_leader,
                    "players": party,
                },
                to = data["partyId"]
            )
        else:
            emit(
                "error",
                {
                    "message": "player could not join party, either it didn't exist or they are in a party already"
                },
            )
    except Exception as e:
        emit("error", {"message": e})


@socketio.on("leave-party")
def leave_party(data):
    """Attempt to leave a party"""
    try:
        success, party = clients.leave_party(data["partyId"], data["clientId"])
        party_leader = party[0]

        if success:
            leave_room(data["partyId"])
            emit(
                "left-party",
                {
                    "partyId": data["partyId"],
                    "clientId": data["clientId"],
                    "partyLeader": party_leader,
                    "players": party,
                },
                to = data["partyId"]
            )
        else:
            emit(
                "error",
                {
                    "message": "player could not leave party, either it didn't exist or they aren't in a party"
                },
            )
    except Exception as e:
        emit("error", {"message": e})
