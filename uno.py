from enum import IntFlag
import random


class Card(IntFlag):
    """ Flags for different parts of an uno card
    """
    CL_RED = 1<<0
    CL_GREEN = 1<<1
    CL_YELLOW = 1<<2
    CL_BLUE = 1<<3

    V_0 = 1<<5
    V_1 = 1<<6
    V_2 = 1<<7
    V_3 = 1<<8
    V_4 = 1<<9
    V_5 = 1<<10
    V_6 = 1<<11
    V_7 = 1<<12
    V_8 = 1<<13
    V_9 = 1<<14
    V_STOP = 1<<15
    V_REVERSE = 1<<16
    V_PLUS_TWO = 1<<17
    V_PLUS_FOUR = 1<<18
    V_CHANGE_COLOUR = 1<<19

    def __repr__(self) -> str:
        vals = self.name.replace('CL_', '').split("|")
        if len(vals) > 1:
            return f"{vals[0].capitalize()} {vals[1].replace('V_', '').capitalize().replace('_', ' ')}"
        else:
            return f"Wildcard: {vals[0].replace('V_', '')}"



# Uno Constants
global ALL_COLOURS, NUMERICAL_VALUES, BASE_UNO_DECK
ALL_COLOURS = (Card.CL_BLUE, Card.CL_GREEN, Card.CL_RED, Card.CL_YELLOW)
ALL_NUMBERS = (Card.V_0, Card.V_1, Card.V_2, Card.V_3, Card.V_4, Card.V_5,
               Card.V_6, Card.V_7, Card.V_8, Card.V_9, Card.V_STOP, Card.V_PLUS_TWO, Card.V_REVERSE)
NUMERICAL_VALUES = (Card.V_0)
BASE_UNO_DECK: (int) = tuple(
    [val | col for val in ALL_NUMBERS for i in range(2) for col in ALL_COLOURS] + 
    [Card.V_CHANGE_COLOUR for i in range(4)] + 
    [Card.V_PLUS_FOUR for i in range(4)]
)


class Uno:

    def __init__(self, num_players: int):

        self.num_players = num_players
        # Game setup
        self.draw_pile = self.randomise_cards()
        self.user_hands = list([] for i in range(num_players))

        self.deal_hands(self.num_players)
        self.discard_pile = [self.draw_next_card()]                # stack
        
        self.winner = -1            # updated when someone wins the game
        self.current_player = 0     # index of the current player
        self.next_player = 1        # needed as can be skipped by certain cards
        self.reversed = False

        self.play_game()


    def play_game(self) -> None:
        """Plays a single game of uno with the hands dealt and the players selected

        args:
            None

        returns:
            None
        """
        while self.winner == -1:
            self.take_turn(self.current_player, self.next_player)
            self.update_player_index()
    
    def update_player_index(self) -> None:
        """ Updates the current and next player based on the current rules in play
        
        args:
            None

        returns:
            None
        """
        self.current_player = self.next_player
        n_player = self.current_player - 1 if self.reversed else self.current_player + 1
        self.next_player = n_player % self.num_players
    
    def take_turn(self, current_player: int, next_player: int) -> None:
        """Takes a turn given the current player and the player that will bare the 
        results of the player's actions

        args:
            current_player(int): player that is currently playing their turn
            next_player(int): player that is to the left of the current player
        """
        # if the user cannot play a card then they 
        if not self.can_play(current_player):
            self.give_cards(current_player, 1)
        
        # get the card that the user wishes to play
        card = self.user_hands[current_player].pop(self.get_user_choice(current_player))
        # if they cannot play it then try this function again
        if not self.can_play_card(card):
            print(f"Cannot play {card} on {self.get_top_card()}")
        
        # since they can play the card, do the actions
        self.discard_pile.append(card)

        self.do_card(card, next_player)


    def do_card(self, card: int, next_player: int):
        """ Applies the result of a special card
        """
        if card & Card.V_PLUS_FOUR:
            self.give_cards(next_player, 4)
        elif card & Card.V_PLUS_TWO:
            self.give_cards(next_player, 2)
        elif card & Card.V_STOP:
            self.next_player = (next_player + 1)%self.num_players
        elif card & Card.V_REVERSE:
            self.reversed = not self.reversed


    def can_play(self, player: int) -> bool:
        return any(map(self.can_play_card, self.user_hands[player]))


    def get_user_choice(self, player: int) -> int:
        hand = self.user_hands[player]
        print(f"Your cards are: {hand}")
        return int(input("What do you want to play? >> "))
    

    def get_top_card(self) -> Card:
        """ Gets the card that is currently facing the board
        """
        return self.discard_pile[-1]


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
        top_card = self.get_top_card()
        return Uno.are_same_colour(played_card, top_card) or \
                Uno.are_same_value(played_card, top_card) or\
                Uno.is_wildcard(played_card)
    
    def draw_next_card(self) -> Card:
        """Draw the next card from the draw pile
        """
        return self.draw_pile.pop(-1)
    
    def give_cards(self, player: int, num_cards: int) -> None:
        self.user_hands[player] += [self.draw_next_card() for i in range(num_cards)]
    
    def deal_hands(self, num_players: int) -> [Card]:
        """ Draws 7 cards for each player
        """
        for player in range(num_players):
            self.give_cards(player, 7)
    
    @staticmethod
    def are_same_colour(card1: int, card2: int) -> bool:
        """ Checks if two cards have the same colour flag bit set

        args:
            card1: The first card to perform the comparison with
            card2: The second card to perform the comparison with
        
        returns:
            true if the cards have the same colour, otherwise false
        """
        mask = 15
        return card1 & mask == card2 & mask

    @staticmethod
    def are_same_value(card1: int, card2: int) -> bool:
        mask = (1<<18 - 1) &~15
        return card1 & mask == card2 & mask

    @staticmethod
    def is_wildcard(card: int) -> bool:
        return not card & 15
    
if __name__ == "__main__":
    print(Uno.are_same_colour(Card.CL_BLUE, Card.CL_BLUE))
    print(Uno.are_same_colour(Card.CL_BLUE, Card.CL_GREEN))
    u = Uno(3)