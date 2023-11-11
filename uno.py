from dataclasses import dataclass
from enum import IntFlag
import random


class Card(IntFlag):
    CL_RED = 0
    CL_GREEN = 1<<0
    CL_YELLOW = 1<<1
    CL_BLUE = 1<<2

    V_0 = 1<<3
    V_1 = 1<<4
    V_2 = 1<<5
    V_3 = 1<<6
    V_4 = 1<<7
    V_5 = 1<<8
    V_6 = 1<<9
    V_7 = 1<<10
    V_8 = 1<<11
    V_9 = 1<<12
    V_STOP = 1<<13
    V_REVERSE = 1<<14
    V_PLUSTWO = 1<<15
    V_PLUSFOUR = 1<<16
    V_CHANGECOLOUR = 1<<17


# Uno Constants
global ALL_COLOURS, NUMERICAL_VALUES, BASE_UNO_DECK
ALL_COLOURS = (Card.CL_BLUE, Card.CL_GREEN, Card.CL_RED, Card.CL_YELLOW)
NUMERICAL_VALUES = (Card.V_0)
BASE_UNO_DECK: (int) = (
    Card.V_0 | random.choice(ALL_COLOURS) for i in range(108)
) # just a bunch of 0s for now


class Uno:

    def __init__(self, num_players: int):

        self.num_players = num_players
        # Game setup
        self.draw_pile = self.randomise_cards()
        self.user_hands = list([] for i in range(num_players))

        self.deal_hands(self.num_players)
        self.discard_pile = self.draw_next_card()                # stack
        
        self.winner = -1            # updated when someone wins the game
        self.current_player = 0     # index of the current player

        self.play_game()
    

    def play_game(self):
        while self.winner == -1:
            next_player = (current_player + 1) % self.num_players
            self.take_turn(self.current_player, next_player)
            current_player = next_player
    
    def take_turn(self, current_player: int, next_player: int):
        """Takes a turn given the current player and the player that will bare the 
        results of the player's actions

        args:
            current_player(int): player that is currently playing their turn
            next_player(int): player that is to the left of the current player
        """
        # if the user cannot play a card then they 
        if not self.can_play(current_player):
            self.give_cards(current_player, 1)
        card = self.user_hands[current_player].pop(self.get_user_choice())
        if not self.can_play_card(card):
            self.take_turn(current_player, next_player)

    def can_play(self, player: int):
        return any(map(self.can_play_card, self.user_hands[player]))


    def get_user_choice(self, player: int) -> int:
        return random.randint(0, len(self.user_hands[player]))
    

    def get_top_card(self) -> Card:
        """ Gets the card that is currently facing the board
        """
        return self.card_stack[-1]


    def randomise_cards(self) -> [int]:
        """ Gets an entire deck of Uno cards in a random order
        TODO: implement :D
        """
        global BASE_UNO_DECK
        r_val = list(BASE_UNO_DECK)
        random.shuffle(r_val)
        return r_val
    
    
    def can_play_card(self, played_card: Card) -> bool:
        """ Checks if the played card is allowed based on the current top card

        args:
            played_card (Card): the card that is being played (duh)

        EITHER: 
        
        returns:
            bool: can the card be played?
        """
        return False
    
    def draw_next_card(self) -> int:
        """Draw the next card from the draw pile
        """
        return self.draw_pile.pop(-1)
    
    def give_cards(self, player: int, num_cards: int) -> None:
        self.user_hands[player] += [self.draw_next_card for i in range(num_cards)]
    
    def deal_hands(self, num_players: int) -> [Card]:
        """ Draws 7 cards for each player
        """
        for player in range(num_players):
            self.give_cards(player, 7)
    
    @staticmethod
    def are_same_colour(card1: int, card2: int) -> bool:
        return card1 & COLOUR_MASK == card2 & COLOUR_MASK
    
if __name__ == "__main__":
    u = Uno(3)