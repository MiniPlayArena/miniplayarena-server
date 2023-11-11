import uuid
from flask_socketio import emit, join_room, leave_room
from __main__ import socketio, clients

@socketio.on("connect")
def connection():
    print("Client connected!")


@socketio.on("disconnect")
def disconnect():
    print("Client disconnected!")


@socketio.on("get-uuid")
def get_uuid():
    client_uuid = uuid.uuid4()
    emit("set-uuid", {"uuid": str(client_uuid)})
    print(f"Generated new UUID: {client_uuid}")


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
        party_leader = None if party is None else list(party.keys())[0]

        if success:
            join_room(party_id)
            emit(
                "party-created",
                {
                    "partyId": party_id,
                    "partyLeader": party_leader,
                    "players": party
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
        party_leader = None if party is None else list(party.keys())[0]

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
        party_leader = None if party is None else list(party.keys())[0]

        if success:
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
            leave_room(data["partyId"])
        else:
            emit(
                "error",
                {
                    "message": "player could not leave party, either it didn't exist or they aren't in a party"
                },
            )
    except Exception as e:
        emit("error", {"message": e})


@socketio.on("create-game")
def create_game(data):
    """Attempt to create game"""
    try:
        success, party, err = clients.create_game(data["partyId"], data["clientId"], data["gameId"])
        party_leader = None if party is None else list(party.keys())[0]

        if success:
            emit(
                "game-created",
                {
                    "partyId": data["partyId"],
                    "gameId": data["gameId"],
                    "firstPlayer": party_leader
                },
                to = data["partyId"]
            )
        elif err is not None:
            emit(
                "error",
                {
                    "message": err
                }
            )
        else:
            emit(
                "error",
                {
                    "message": "game was not created, most likely because a game has already been created"
                },
            )
    except Exception as e:
        emit("error", {"message": e})


@socketio.on("get-game-state")
def get_game_state(data):
    """Allows the user to get the games state"""
    try:
        success, game_state = clients.get_game_state(data["partyId"], data["clientId"], data["gameId"])

        if success:
            emit(
                "game-state",
                {
                    "partyId": data["partyId"],
                    "gameId": data["gameId"],
                    "gameState": game_state
                }
            )
        else:
            emit(
                "error",
                {
                    "message": "game state could not be found, is a game being played?"
                }
            )
    except Exception as e:
        emit("error", {"message", e})


@socketio.on("updated-game-state")
def update_game_state(data):
    """Updates the game state if possible"""
    try:
        success, game_state, error_message = clients.update_game_state(data["partyId"], data["clientId"], data["gameState"])

        if success:
            emit(
                "game-state",
                {
                    "partyId": data["partyId"],
                    "gameId": data["gameId"],
                    "gameState": game_state
                }
            )
            emit(
                "new-game-state-available",
                {
                    "partyId": data["partyId"],
                    "gameId": data["gameId"],
                    "lastMove": data["clientId"] 
                },
                to = data["partyId"]
            )
        else:
            emit(
                "error",
                {
                    "message": error_message
                }
            )
    except Exception as e:
        emit("error", {"message": e})


@socketio.on("delete-game")
def delete_game(data):
    """Delete the game"""
    try:
        success = clients.delete_game(data["partyId"])

        if success:
            emit(
                "game-over",
                {
                    "partyId": data["partyId"]
                },
                to = data["partyId"]
            )
        else:
            emit(
                "error",
                {
                    "message": "game could not be stopped, this could be due to the game not existing"
                }
            )
    except Exception as e:
        emit("error", {"message": e})