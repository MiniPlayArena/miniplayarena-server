from games.game import Game
import random


class SnakesAndLadders(Game):
    def __init__(self, players: [str]):
        super().__init__(4, "Snakes and Ladders", players)
        # If a board number has a value, then landing on that square jumps you to the position
        self.snakes_and_ladders = {
            97: 78,
            95: 56,
            88: 24,
            62: 18,
            36: 6,
            32: 10,
            48: 26,
            80: 99,
            71: 92,
            50: 67,
            28: 76,
            8: 30,
            1: 38,
            4: 14,
            21: 42,
        }
        self.player_positions = {player: 1 for player in self.players}

    def get_client_data(self, player: int) -> dict:
        """Returns the game state for a specific client

        args:
            player(int): the player to get the game state for

        returns:
            dictionary with the client data
                For snakes and ladders, this is in the format
                {
                    "player-position": <current-player-position>
                    "other-player-positions": <other-player-positions>
                }
        """
        return {
            "player-position": self.player_positions[player],
            "other-player-positions": dict(
                filter(lambda x: x[0] != player, self.player_positions.items())
            ),
        }

    def take_turn(self, player: int, turn_data: dict):
        # this is snakes and ladders so we literally do not need turn data from the user
        # random roll :D
        roll = random.randint(1, 6)

        # update position
        self.player_positions[player] += roll

        # move up or down if snake or ladder
        pos_to_check = self.player_positions[player]
        if pos_to_check in self.snakes_and_ladders:
            self.player_positions[player] = self.snakes_and_ladders[pos_to_check]

        if pos_to_check == 100:
            self.winner = player

        r_data = self.get_all_client_data()
        r_data.update({"num-rolled": roll})
        return

    def game_is_won(self) -> str:
        return self.winner != "", self.get_final_gamestate()


if __name__ == "__main__":
    s = SnakesAndLadders(2)
