class Clients():
    """Holds al client games"""

    def __init__(self) -> None:
        self.clients = {}
        self.games = {}
        self.parties = {}

    def create_player(self, client_id: str, username: str) -> bool:
        """Add player to clients list"""
        if client_id not in self.clients.keys():
            self.clients[client_id] = username
            print(f"Added player! {client_id} => {username}")
            return True
        return False

    def create_party(self, party_name: str, player_id: str) -> bool:
        """Create a party with at least 1 player"""
        if player_id in self.clients.keys():
            self.parties[party_name] = [player_id]
            return True
        return False