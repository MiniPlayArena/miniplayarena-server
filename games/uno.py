from enum import IntFlag
from games.game import Game
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
            return f"{vals[0].capitalize()[0]} {vals[1].replace('V_', '').replace('_', ' ').capitalize()}"
        else:
            return f"Wildcard: {vals[0].replace('V_', '').replace('_', ' ').capitalize()}"
    
    def __str__(self) -> str:
        return self.__repr__()



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


class Uno(Game):

    def __init__(self, players: [str]):

        super().__init__(10, "Uno", players)
        
        # Game setup
        self.draw_pile = self.randomise_cards()
        self.user_hands = {player: [] for player in self.players}

        self.deal_hands(self.num_players)
        self.discard_pile = [self.draw_next_card()]                # stack

        # inits
        self.next_player = 1        # needed as can be skipped by certain cards
        self.reversed = False
        self.c_col_card = None

         # apply the result of the first card
        self.do_card(self.get_top_card(), 0)
    
    def take_turn(self, current_player: str, turn_data: dict) -> bool:
        """Takes a turn given the current player and the player that will bare the 
        results of the player's actions

        args:
            current_player(int): player that is currently playing their turn
            turn_data(int): the data for the turn that the player has submitted.
                For Uno, this should be in the format {
                    played_card: <played-card>
                }
                where <played-card> is the index of the card that the player has attempted to play
        """

        r_data = self.get_all_client_data()

        # if the current player is not the one that is allowed to play
        if current_player != self.current_player:
            r_data["game-state"][current_player].update({"display-message": "It is not your turn you gimp"})
            return r_data
            
        # if the user cannot play a card then they 
        if not self.can_play(current_player):
            self.give_cards(current_player, 1)
            self.update_player_index()
            r_data["game-state"][current_player].update({"display-message": "You cannot play. Unlucky :D"})
        
        # get the card that the user wishes to play
        played_card = int(turn_data["played-card"])
        if played_card < 0 or played_card >= len(self.user_hands[current_player]):
            r_data["game-state"][current_player].update({"display-message": "Error.."})
            return r_data
        
        card = self.user_hands[current_player].pop()
        # if they cannot play it then try this function again
        if not self.can_play_card(card):
            # re-add card to hand and return
            self.user_hands[current_player].append(card)
            r_data["game-state"][current_player].update({"display-message": "Cannot play that card idiot"})
        
        # since they can play the card, do the actions
        self.discard_pile.append(card)
        self.do_card(card, self.next_player)

        # update current player and next player pointers
        self.update_player_pointers(self.reversed)

        # re-generate data as the state has changed
        return self.get_all_client_data()

    def has_won(self, player: int) -> bool:
        return len(self.user_hands[player]) == 0

    def game_is_won(self) -> bool:
        return any(map(self.has_won, range(self.num_players)))

    def do_card(self, card: int, next_player: int):
        """ Applies the result of a special card
        """
        if card & Card.V_PLUS_FOUR:
            self.give_cards(next_player, 4)
            self.change_colour()
        elif card & Card.V_PLUS_TWO:
            #TODO: Implement logic for stacking +2s
            self.give_cards(next_player, 2)
        elif card & Card.V_STOP:
            self.next_player = (next_player + 1)%self.num_players
        elif card & Card.V_REVERSE:
            self.reversed = not self.reversed
            n_player = self.next_player - 1 if self.reversed else self.next_player + 1
            self.next_player = n_player % self.num_players
        elif card & Card.V_CHANGE_COLOUR:
            self.change_colour()


    def can_play(self, player: int) -> bool:
        """Checks if a player can actually place a card

        args:
            player(int): the player to check

        return:
            (bool) whether or not the player can play
        """
        return any(map(self.can_play_card, self.user_hands[player]))


    def get_user_choice(self, player: int) -> int:
        print(f"\nThe top card is {self.get_top_card()}, player {player} what do you play?")
        hand = self.user_hands[player]
        print(f"Your cards are: {hand}")
        return int(input("What do you want to play? >> "))
    

    def get_top_card(self) -> Card:
        """ Gets the card that is currently facing the board
        """
        c = Card(self.discard_pile[-1])
        return c


    def randomise_cards(self) -> [int]:
        """ Gets an entire deck of Uno cards in a random order
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

        # if the colour was just changed, only check for colour
        if top_card & Card.V_PLUS_FOUR or top_card & Card.V_CHANGE_COLOUR:
            return Uno.are_same_colour(played_card, self.c_col_card)

        # else check for same colour, value or wildcard being played
        return Uno.are_same_colour(played_card, top_card) or \
                Uno.are_same_value(played_card, top_card) or\
                Uno.is_wildcard(played_card)
    
    def draw_next_card(self) -> Card:
        """Draw the next card from the draw pile
        """
        return self.draw_pile.pop(-1)
    
    def give_cards(self, player: int, num_cards: int) -> None:
        """Adds a number of cards to the player's hand

        args:
            player(int): the player to add the cards to
            num_cards(int): the number of cards to give the player
        
        returns:
            None
        """
        self.user_hands[self.get_player_id(player)] += [self.draw_next_card() for i in range(num_cards)]
    
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
        """Checks if two cards have the same value (excluding +4 and colour change)

        args:
            card1: The first card to perform the comparison with
            card2: The second card to perform the comparison with
        
        returns:
            true if the cards have the same value, otherwise false
        """
        mask = ((1<<18) - 1) &~15
        return card1 & mask == card2 & mask

    @staticmethod
    def is_wildcard(card: int) -> bool:
        """Checks if a card is a wildcard
        In reality, just checks if a card has a colour bit assigned to it, if not then it must be a wildcard

        args:
            card(int): the card to check
        
        returns:
            bool: whether the card is a wildcard (+4 or colour change)
        """
        return not card & 15


    def change_colour(self) -> None:
        """ Changes the colour without changing the top card, as needed when +4 and colour change
        cards are used

        args:
            None

        returns:
            The card with just the colour
        """
        self.c_col_card =  Card(int(input("What colour? 1, 2, 4 or 8")))
    

    def get_client_data(self, player: str) -> dict:
        """For Uno, the player data that is needed for each individual client is:
        The current top of the discard pile (c_facing_card)
        And the player's current hand (c_hand)
        """
        return {
            "next_player": self.get_player_id(self.next_player),
            "c_facing_card": self.get_top_card(),
            "c_hand": [
                str(card) for card in self.user_hands[player]
            ]
        }
    