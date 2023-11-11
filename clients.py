import secrets


class Clients:
    """Holds al client games"""

    def __init__(self) -> None:
        self.clients = {}
        self.games = {}
        self.parties = {}

    def get_player_name(self, player_id: str):
        """Attempt to get player name"""
        if player_id in self.clients.keys():
            return self.clients[player_id]
        return "not found"

    def create_player(self, client_id: str, username: str) -> bool:
        """Add player to clients list"""
        if client_id not in self.clients.keys() and len(username) > 3:
            self.clients[client_id] = username
            print(f"Added player! {client_id} => {username}")
            return True
        return False

    def create_party(self, party_leader: str) -> bool:
        """Create a party with at least 1 player"""
        if party_leader in self.clients.keys():
            print("Checking if player is in a party...")
            for party in self.parties:
                if party_leader in party:
                    return False, None

            print("Creating party...")
            party_id = make_random_not_in_list(self.parties.keys())
            self.parties[party_id] = [party_leader]
            print(f"Party created {party_id} => {self.clients[party_leader]}")
            return True, party_id, [self.clients[party_leader]]
        return False, None

    def join_party(self, party_id: str, client_id: str):
        """Try make a user join a party"""
        if client_id in self.clients.keys():
            print("Checking if player is in a party...")
            for party in self.parties:
                if client_id in party:
                    return False, None

            print("Player can join a party, checking if party exists...")
            if (
                party_id in self.parties.keys()
                and client_id not in self.parties[party_id]
            ):
                self.parties[party_id].append(client_id)
                print(f"Added player to party => {self.parties[party_id]}")
                return True, [self.clients[client] for client in self.parties[party_id]]
            
            print("Party does not exist")
        return False, None

    def leave_party(self, party_id: str, client_id: str):
        """Try make a user leave a party"""
        if client_id in self.clients.keys():
            print("Checking if player is in a party...")
            for party in self.parties:
                if client_id in party:
                    print("Player can leave a party, checking if party exists...")
                    if client_id in party:
                        party.remove(client_id)
                        print(f"Removed player from party => {party}")
                        return True, [self.clients[client] for client in self.parties[party_id]]
            print("Party does not exist")
        return False, None


def make_random_not_in_list(list: list, length: int = 3):
    """Try find a random code that is not in a list"""
    found = False
    while not found:
        test_code = secrets.token_hex(length).upper()
        if test_code not in list:
            found = True
            return test_code
