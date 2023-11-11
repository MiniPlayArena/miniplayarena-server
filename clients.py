import secrets
from games.game import create_game as cg

class Clients:
    """Holds al client games"""

    def __init__(self) -> None:
        self.clients = {}
        self.games = {}
        self.parties = {}

        self.valid_games = ["uno", "sal"]

    # USEFUL FUNCTIONS
    def is_user(self, client_id: str):
        return client_id in self.clients.keys()
    
    def is_party(self, party_id: str):
        return party_id in self.parties.keys()
    
    def is_in_party(self, client_id: str, party_id: str):
        return client_id in self.parties[party_id]
    
    def is_leader(self, client_id: str, party_id: str):
        return client_id == self.parties[party_id][0]

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

    def get_party_game(self, party_id: str):
        pass

    # OTHER STUFF

    def create_player(self, client_id: str, username: str) -> bool:
        """Add player to clients list"""
        if not self.is_user(client_id) and len(username) > 3:
            self.clients[client_id] = username
            print(f"Added player! {client_id} => {username}")
            return True
        return False

    def create_party(self, party_leader: str) -> bool:
        """Create a party with at least 1 player"""
        if self.is_user(party_leader):
            print("Checking if player is in a party...")
            if self.is_in_any_party(party_leader):
                return False, None

            # Create party
            print("Creating party...")
            party_id = make_random_not_in_list(self.parties.keys())
            self.parties[party_id] = [party_leader]
            print(f"Party created {party_id} => {self.clients[party_leader]}")
            return True, party_id, self.create_party_output(party_id)
        return False, None

    def join_party(self, party_id: str, client_id: str):
        """Try make a user join a party"""
        if self.is_user(client_id):
            print("Checking if player is in a party...")
            if self.is_in_any_party(client_id):
                return False, None

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
                    game = cg(game_id, self.clients.keys())
                    print(game)
        return False, None
    
    def get_game_state(self, party_id: str, client_id: str, game_id: str):
        """Returns the current game state for that player"""
        pass

    def update_game_state(self, party_id: str, client_id: str, game_id: str, game_state):
        """Attempts to update game state"""
        pass


# Other useful functions
def make_random_not_in_list(list: list, length: int = 3):
    """Try find a random code that is not in a list"""
    found = False
    while not found:
        test_code = secrets.token_hex(length).upper()
        if test_code not in list:
            found = True
            return test_code
