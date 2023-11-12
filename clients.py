import secrets
from games.game import create_game as cg
from games.game import Game

class Clients:
    """Holds al client games"""

    def __init__(self) -> None:
        self.clients = {}
        self.games = {}
        self.parties = {}

        self.valid_games = ["uno", "snakes_ladders"]

    # USEFUL FUNCTIONS
    def is_user(self, client_id: str):
        return client_id in self.clients.keys()
    
    def is_party(self, party_id: str):
        return party_id in self.parties.keys()
    
    def is_in_party(self, client_id: str, party_id: str):
        return client_id in self.parties[party_id]
    
    def is_leader(self, client_id: str, party_id: str):
        return client_id == self.parties[party_id][0]
    
    def is_game_playing(self, party_id: str):
        return party_id in self.games.keys()

    def get_player_name(self, player_id: str):
        """Attempt to get player name"""
        if player_id in self.clients.keys():
            return self.clients[player_id]
        return "not found"
    
    def is_in_any_party(self, client_id: str):
        for party in self.parties:
            if client_id in self.parties[party]:
                return True
        return False
    
    def create_party_output(self, party_id: str):
        out = {}
        if self.is_party(party_id):
            for client in self.parties[party_id]:
                out[client] = self.get_player_name(client)
        return out

    def kick_from_party(self, client_id: str):
        for party in self.parties:
            if client_id in self.parties[party]:
                self.parties[party].remove(client_id)
                if self.parties[party] == []:
                    print("Deleting empty party!")
                    self.parties.pop(party)
                return

    # OTHER STUFF
    def create_player(self, client_id: str, username: str) -> bool:
        """Add player to clients list"""
        if client_id is not None and 12 > len(username) > 3:
            self.clients[client_id] = username
            print(f"Added player! {client_id} => {username}")
            return True
        return False

    def create_party(self, party_leader: str) -> bool:
        """Create a party with at least 1 player"""
        if self.is_user(party_leader):
            print("Checking if player is in a party...")
            if self.is_in_any_party(party_leader):
                print("Kicking player from old party!")
                self.kick_from_party(party_leader)

            # Create party
            print("Creating party...")
            party_id = make_random_not_in_list(self.parties.keys())
            self.parties[party_id] = [party_leader]
            print(f"Party created {party_id} => {self.clients[party_leader]}")
            return True, party_id, self.create_party_output(party_id)
        return False, None, None

    def join_party(self, party_id: str, client_id: str):
        """Try make a user join a party"""
        if self.is_user(client_id):
            print("Checking if player is in a party...")
            if self.is_in_any_party(client_id):
                print("Kicking player from old party!")
                self.kick_from_party(client_id)

            print("Player can join a party, checking if party exists...")
            if self.is_party(party_id) and not self.is_in_party(client_id, party_id):
                self.parties[party_id].append(client_id)

                print(f"Added player to party => {self.parties[party_id]}")
                return True, self.create_party_output(party_id)
            
            print("Party does not exist")
        return False, None

    def leave_party(self, party_id: str, client_id: str):
        """Try make a user leave a party"""
        if self.is_user(client_id):
            print("Checking if player is in a party...")
            if self.is_party(party_id) and self.is_in_party(client_id, party_id):
                party = self.parties[party_id]
                party.remove(client_id)

                print(f"Removed player from party => {party}")
                if party != []:
                    return True, self.create_party_output(party_id)
                else:
                    print("Party is cleared!")
                    self.parties.pop(party_id)
                    return True, None
            print("Party does not exist")

        return False, None
    
    def create_game(self, party_id: str, client_id: str, game_id: str):
        """Attempt to create a game"""
        if self.is_user(client_id) and self.is_leader(client_id, party_id):
            print("Checking if player is in party and is party leader...")
            if self.is_party(party_id) and self.is_in_party(client_id, party_id):
                print("Checking if game id is valid!")
                
                # Check if game is valid and attempt to create
                if game_id in self.valid_games:
                    if self.is_game_playing(party_id):
                        return True, self.create_party_output(party_id), None
                    else:
                        game, err = cg(game_id, list(self.clients.keys()))
                        print(f"Game created: {game}")
                        if game is not None:
                            self.games[party_id] = game
                            return True, self.create_party_output(party_id), None
                    return False, None, err
        return False, None, None
    
    def get_game_state(self, party_id: str, client_id: str):
        """Returns the current game state for that player"""
        if self.is_user(client_id):
            print("Checking if the player is in the correct party...")
            if self.is_party(party_id) and self.is_in_party(client_id, party_id):
                print("Checking if correct game is being played")

                # Return correct game if found
                if self.is_game_playing(party_id):
                    print("Game found, sending game state!")
                    game: Game = self.games[party_id]
                    game_status = game.get_client_data(client_id)
                    return True, game_status
        return False, None

    def update_game_state(self, party_id: str, client_id: str, game_state):
        """Attempts to update game state"""
        if self.is_user(client_id):
            print("Checking if user is in correct party...")
            if self.is_party(party_id) and self.is_in_party(client_id, party_id):
                print("Checking if correct game is being played")

                # Update game status
                if self.is_game_playing(party_id):
                    print("Game found, sending game status!")
                    game: Game = self.games[party_id]
                    game_status = game.take_turn(client_id, game_state)

                    # Check if game is won
                    has_won, won_status = game.game_is_won()
                    if has_won:
                        print("Game is over!")
                        return True, won_status
                    return True, game_status
        return False, None
    
    def delete_game(self, party_id: str, client_id: str):
        if self.is_user(client_id):
            print("Checking if user is in correct party...")
            if self.is_party(party_id) and self.is_in_party(client_id, party_id):
                print("Checking if game exists...")

                if self.is_game_playing(party_id):
                    self.games.pop(party_id)
                    print("Game has been deleted!")
                    return True
        return False


# Other useful functions
def make_random_not_in_list(list: list, length: int = 1):
    """Try find a random code that is not in a list"""
    found = False
    while not found:
        test_code = secrets.token_hex(length).upper()
        if test_code not in list:
            found = True
            return test_code
