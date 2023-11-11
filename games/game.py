

class Game:

    def __init__(self, max_players: int, name: str, min_players: int = 2):
        self.player_constraints = (min_players, max_players)
        self.name = name
        self.current_player = 0
    

    def get_active_player(self) -> int:
        """Gets the player who's turn it is next.

        args:
            None
        
        returns:
            (int): The player that is next to play
        """
        return self.current_player

    def get_client_data(self, player: int) -> dict:
        """Gets all the data that the player needs at a given time point as a JSON encoded dict

        Call this when you want to get all the data that is relevant to a certain client's
        frontend stuff

        args:
            player(int): index of the player to get the data for
        
        returns:
            JSON encoded data :D
        """
        raise NotImplementedError("Implement this please :DDD")

    def update_game_data(self, incoming_player: int, data: dict) -> None:
        """Updates the game state based on what the player has sent

        Call this when you want to update the state of the game on the server based on the inputs
        of the player

        args:
            incoming_player(int): the id of the player that has sent the information
            data(dict): json-encoded data 
        """
        raise NotImplementedError("Implement this one too :(")

    def is_valid_playercount(self, players: int) -> bool:
        """ Checks if the given number of players is allowed

        args:
            players(int): the number of players that the game is trying to be initialised with
        
        returns:
            is the player count valid
        """
        return self.player_constraints[0] <= players <= self.player_constraints[1]
        