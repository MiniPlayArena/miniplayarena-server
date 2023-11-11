from typing import Optional

class Game:

    def __init__(self, max_players: int, name: str, player_ids: str, min_players: int = 2):
        
        self.player_constraints = (min_players, max_players)
        self.num_players = len(player_ids)
        self.players = player_ids

        self.name = name
        self.current_player = 0
        self.winner = -1
        
    

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
        
        Called at the end of take_turn, but can be called whenever you want to explicitly
        get data to update a certain client (for whatever reason)

        Call this when you want to get all the data that is relevant to a certain client's
        frontend stuff, so probably whenever the game state has changed

        args:
            player(int): index of the player to get the data for
        
        returns:
            JSON encoded data :D
        """
        raise NotImplementedError("Implement this please :DDD")

    def get_all_client_data(self) -> dict:
        """Gets all the data for ALL the clients and returns in JSON format

        args:
            None

        returns:
            Json dictionary with the entire game state. Dont send this to all players please :D
        """
        return {"game-state": [self.get_client_data(i) for i in range(self.num_players)]}

    def take_turn(self, incoming_player: int, turn_data: dict) -> dict:
        """Updates the game state based on what the player has sent

        Call this when you want to update the state of the game on the server based on the inputs
        of the player

        args:
            incoming_player(int): the id of the player that has sent the information
            turn_data(dict): json-encoded data of the turn that the player would make (should be
            generated by frontend probably)
        
        returns:
            a dictionary containing the data to send to each client based on the turn that was played
        """
        raise NotImplementedError("Implement this one too :(")

    def is_valid_playercount(self) -> bool:
        """ Checks if the given number of players is allowed

        args:
            players(int): the number of players that the game is trying to be initialised with
        
        returns:
            is the player count valid
        """
        return self.player_constraints[0] <= self.num_players <= self.player_constraints[1]


    def game_is_won(self) -> bool:
        """Gets whether or not the game has been won
        
        args:
            None

        returns:
            The condition of the game
        """
        raise NotImplementedError("Please implement a win condition")

    def remove_player(self, player: str) -> None:
        """Removes a player from the game in the case of a disconnect

        args:
            player(str): the id of the player to be removed
        """
        raise NotImplementedError("Please implement player removal logic")


def create_game(game_id: str, players: [str]) -> Optional[Game]:
    """Creates a game given the game id and the players present in the party

    args:
        game_id(str): the id of the game that should be played
        players(list(str)): the list of player ids
    
    returns:
        a game if the player count was valid, else returns None
    """
    r_val = None
    if game_id == "uno":
        import uno
        r_val = uno.Uno(players)
    elif game_id == "sal":
        import sal
        r_val =  sal.SnakesAndLadders(players)
    
    return None if (not r_val or not r_val.is_valid_playercount()) else r_val
