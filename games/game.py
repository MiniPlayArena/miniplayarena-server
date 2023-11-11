

class Game:

    def __init__(self, max_players: int, name: str, min_players: int = 2):
        self.player_constraints = (min_players, max_players)
        self.name = name

    def get_player_data(self, player: int) -> dict:
        """Gets all the data that the player needs at a given time point as a JSON encoded dict

        args:
            player(int): index of the player to get the data for
        
        returns:
            JSON encoded data :D
        """
        raise NotImplementedError("Implement this please :DDD")

    def is_valid_playercount(self, players: int) -> bool:
        """ Checks if the given number of players is allowed

        args:
            players(int): the number of players that the game is trying to be initialised with
        
        returns:
            is the player count valid
        """
        return self.player_constraints[0] <= players <= self.player_constraints[1]
        