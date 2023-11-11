from dataclasses import dataclass
from enum import IntEnum


class Color(IntEnum):
    CL_WILDCARD = 0
    CL_RED = 1
    CL_YELLOW = 2
    CL_GREEN = 3
    CL_BLUE = 4

class CardValue(IntEnum):
    C_0 = 0
    C_1 = 1
    C_2 = 2
    C_3 = 3
    C_4 = 4
    C_5 = 5
    C_6 = 6
    C_7 = 7
    C_8 = 8
    C_9 = 9
    C_REVERSE = 10
    C_STOP = 11
    C_PLUSTWO = 12
    C_PLUSFOUR = 13
    C_CHANGECOLOUR = 14


@dataclass
class Card:
    colour: Color
    vaule: str # ? do we want enum or just char


class Uno:

    def __init__(self, num_players: int):

        self.num_players = num_players

        # Game setup
        self.card_stack: [Card] = self.randomise_cards()
        self.user_hands: ([Card]) = self.deal_cards(self.num_players)
        
        self.winner = -1            # updated when someone wins the game
        self.current_player = 0     # index of the current player

        self.play_game()
    

    def play_game(self):
        while self.winner == -1:
            next_player = self.can_play_card
            self.take_turn(self.current_player, next_player)
    

    def take_turn(self, current_)

    

    def get_top_card(self) -> Card:
        """ Gets the card that is currently facing the board
        """
        return self.card_stack[-1]


    def randomise_cards(self) -> [Card]:
        """ Gets an entire deck of Uno cards in a random order
        TODO: implement :D
        """
        return []
    
    
    def can_play_card(self, played_card: Card) -> bool:
        """ Checks if the played card is allowed based on the current top card

        args:
            played_card (Card): the card that is being played (duh)

        EITHER: 
        
        returns:
            bool: can the card be played?
        """
        return False
    
    def give_cards(self, player: int, num_cards: int) -> None:

    
    def deal_hands(self, num_players: int) -> [Card]:
        """ Generates a random
        """
        return 