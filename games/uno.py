from enum import IntFlag
from games.game import Game
import random

class Card(IntFlag):
    """Flags for different parts of an uno card"""

    CL_RED = 1 << 0
    CL_GREEN = 1 << 1
    CL_YELLOW = 1 << 2
    CL_BLUE = 1 << 3

    V_0 = 1 << 5
    V_1 = 1 << 6
    V_2 = 1 << 7
    V_3 = 1 << 8
    V_4 = 1 << 9
    V_5 = 1 << 10
    V_6 = 1 << 11
    V_7 = 1 << 12
    V_8 = 1 << 13
    V_9 = 1 << 14
    V_SKIP = 1 << 15
    V_REVERSE = 1 << 16
    V_PLUS_TWO = 1 << 17
    V_PLUS_FOUR = 1 << 18
    V_CHANGE_COLOUR = 1 << 19

    @staticmethod
    def from_packet(c: str):
        if c == "W+":
            return Card.V_PLUS_FOUR
        elif c == "WC":
            return Card.V_CHANGE_COLOUR
        col = f"CL_{c[0].replace('R', 'RED').replace('G', 'GREEN').replace('Y', 'YELLOW').replace('B', 'BLUE')}"

        if c[1] == "+":
            return Card[col] | Card.V_PLUS_TWO
        elif c[1] == "S":
            return Card[col] | Card.V_SKIP
        elif c[1] == "R":
            return Card[col] | Card.V_REVERSE
        else:
            return Card[col] | Card[f"V_{c[1]}"]
        
    def get_colour(self) -> str:
        return self.name.replace("CL_", "").split("|")[0].upper()[0]

    def __repr__(self) -> str:
        vals = self.name.replace("CL_", "").split("|")
        if self & Card.V_SKIP:
            return f"{vals[0].capitalize()[0]}S"
        if self & Card.V_REVERSE:
            return f"{vals[0].capitalize()[0]}R"
        if self & Card.V_PLUS_TWO:
            return f"{vals[0].capitalize()[0]}+"
        if len(vals) > 1:
            return f"{vals[0].capitalize()[0]}{vals[1].replace('V_', '').replace('_', ' ').capitalize()}"
        else:
            return "W+" if self & Card.V_PLUS_FOUR else "WC"

    def __str__(self) -> str:
        return self.__repr__()


# Uno Constants
global ALL_COLOURS, BASE_UNO_DECK
ALL_COLOURS = (Card.CL_BLUE, Card.CL_GREEN, Card.CL_RED, Card.CL_YELLOW)
ALL_NUMBERS = (
    Card.V_0,
    Card.V_1,
    Card.V_2,
    Card.V_3,
    Card.V_4,
    Card.V_5,
    Card.V_6,
    Card.V_7,
    Card.V_8,
    Card.V_9,
    Card.V_SKIP,
    Card.V_PLUS_TWO,
    Card.V_REVERSE,
)
BASE_UNO_DECK: (int) = tuple(
    [val | col for val in ALL_NUMBERS for i in range(2) for col in ALL_COLOURS]
    + [Card.V_CHANGE_COLOUR for i in range(4)]
    + [Card.V_PLUS_FOUR for i in range(4)]
)


class Uno(Game):
    def __init__(self, players: [str]):
        super().__init__(10, "Uno", players)

        # Game setup
        self.draw_pile = self.randomise_cards()
        self.user_hands = {player: [] for player in self.players}

        self.deal_hands(self.num_players)
        self.draw_first_card()
        # inits
        self.reversed = False
        self.c_col_card = None

        # apply the result of the first card TODO: if this is change colour then we are fucked
        self.do_card(self.get_top_card(), 0, {"action-change-colour": 8})


        self.winners = []

    def take_turn(self, current_player: str, turn_data: dict) -> bool:
        """Takes a turn given the current player and the player that will bare the
        results of the player's actions

        args:
            current_player(int): player that is currently playing their turn
            turn_data(int): the data for the turn that the player has submitted.
                For Uno, this should be in the format {
                    played_card: <played-card>
                }
                where <played-card> is the identifier of the card that the player has attempted to play
        """

        print(f"Current player: {current_player}, Next Player: {self.get_player_id(self.next_player)}")
        print(f"Current player: {self.get_player_index(current_player)}, Next Player: {self.next_player}")


        r_data = self.get_all_client_data()

        # if the current player is not the one that is allowed to play
        if current_player != self.get_player_id(self.current_player):
            print("Not current turn")
            r_data["game-state"][current_player][
                "display_message"
            ] = "It is not your turn to play!"
            return r_data

        if "pick-card" in turn_data:
            print("Picking card")
            if not self.give_cards(self.get_player_index(current_player), 1):
                r_data["game-state"][current_player].update(
                        {"display_message": "There are no more cards left in the deck. You are too greedy."}
                    )
                return r_data
            if not self.can_play(current_player):
                self.update_player_pointers()
            return self.get_all_client_data()

        # get the card that the user wishes to play
        played_card = Card.from_packet(turn_data["played_card"])
        print(f"Player {current_player} played card {played_card}")
        if played_card not in self.user_hands[current_player]:
            r_data["game-state"][current_player].update(
                {"display_message": "You cannot play that card as you don't have it"}
            )
            return r_data

        # if they cannot play it then try this function again
        if not self.can_play_card(played_card):
            # re-add card to hand and return
            print("Can't play card :(")
            r_data["game-state"][current_player][
                "display_message"
            ] = "Cannot play that card "
            return r_data

        # since they can play the card, do the actions
        self.discard_pile.append(played_card)
        self.user_hands[current_player].remove(played_card)
        print(f"Turn data: {turn_data}")
        self.do_card(played_card, self.next_player, turn_data)
        print("Played card")
        if len(self.user_hands[current_player]) == 0 and current_player not in self.winners:
            self.winners.append(current_player)
            print(f"Player {current_player} has run out of cards")

        # update current player and next player pointers
        self.update_player_pointers(self.reversed)

        # re-generate data as the state has changed
        return self.get_all_client_data()


    def draw_first_card(self):
        self.discard_pile = [self.draw_next_card()]  # stack

        # make sure first card is not wildcard
        while self.is_invalid_starter(self.get_top_card()):
            self.discard_pile = [self.draw_next_card()]

    def has_won(self, player: int) -> bool:
        return len(self.winners) > (self.num_players - 2)

    def game_is_won(self) -> bool:
        won = len(self.winners) > (len(self.players) - 2)
        return won, self.get_final_gamestate() if won else {}

    def do_card(self, card: int, next_player: int, play_data: dict):
        """Applies the result of a special card"""
        if card & Card.V_PLUS_FOUR:
            self.give_cards(next_player, 4)
            self.c_col_card = self.change_colour(play_data["selected_colour"])
        elif card & Card.V_PLUS_TWO:
            # TODO: Implement logic for stacking +2s
            self.give_cards(next_player, 2)
        elif card & Card.V_SKIP:
            self.increment_next_player(2)
        elif card & Card.V_REVERSE:
            self.reversed = not self.reversed
            self.increment_next_player(1)
        elif card & Card.V_CHANGE_COLOUR:
            self.c_col_card = self.change_colour(play_data["selected_colour"])

    def can_play(self, player: int) -> bool:
        """Checks if a player can actually place a card

        args:
            player(int): the player to check

        return:
            (bool) whether or not the player can play
        """
        return any(map(self.can_play_card, self.user_hands[player]))

    def get_user_choice(self, player: int) -> int:
        print(
            f"\nThe top card is {self.get_top_card()}, player {player} what do you play?"
        )
        hand = self.user_hands[player]
        print(f"Your cards are: {hand}")
        return int(input("What do you want to play? >> "))

    def get_top_card(self) -> Card:
        """Gets the card that is currently facing the board"""
        c = Card(self.discard_pile[-1])
        return c

    def randomise_cards(self) -> [int]:
        """Gets an entire deck of Uno cards in a random order"""
        global BASE_UNO_DECK
        r_val = list(BASE_UNO_DECK)
        random.shuffle(r_val)
        return r_val

    def can_play_card(self, played_card: Card) -> bool:
        """Checks if the played card is allowed based on the current top card

        args:
            played_card (Card): the card that is being played (duh)

        EITHER:

        returns:
            bool: can the card be played?
        """
        top_card = self.get_top_card()

        # if the colour was just changed, only check for colour
        if top_card & Card.V_PLUS_FOUR or top_card & Card.V_CHANGE_COLOUR:
            return Uno.are_same_colour(played_card, self.c_col_card) or Uno.is_wildcard(played_card)

        # else check for same colour, value or wildcard being played
        return (
            Uno.are_same_colour(played_card, top_card)
            or Uno.are_same_value(played_card, top_card)
            or Uno.is_wildcard(played_card)
        )

    def draw_next_card(self) -> Card:
        """Draw the next card from the draw pile"""
        return self.draw_pile.pop(-1)

    def give_cards(self, player: int, num_cards: int) -> None:
        """Adds a number of cards to the player's hand

        args:
            player(int): the player to add the cards to
            num_cards(int): the number of cards to give the player

        returns:
            None
        """
        if len(self.draw_pile) <= num_cards:
                if len(self.discard_pile) == 1:
                   return False
                self.draw_pile = list(reversed(self.discard_pile))
                self.discard_pile = [self.draw_pile.pop(-1)]

        self.user_hands[self.get_player_id(player)] += [
            self.draw_next_card() for i in range(num_cards)
        ]
        return True

    def deal_hands(self, num_players: int) -> [Card]:
        """Draws 7 cards for each player"""
        for player in range(num_players):
            self.give_cards(player, 2)
    
    def increment_next_player(self, num: int) -> None:
        n_player = self.current_player - num if self.reversed else self.current_player + num
        self.next_player = n_player % self.num_players
        if self.get_player_id(self.next_player) in self.winners:
            print(f"Incremembting again as {self.next_player} is a winner")
            self.increment_next_player(1)
        print(f"Inremented to Current player: {self.get_player_id(self.current_player)}, Next Player: {self.get_player_id(self.next_player)}")
        print(f"Inremented to Current player: {self.current_player}, Next Player: {self.next_player}")

    
    def can_still_play(self, player: str) -> bool:
        return len(self.user_hands[player]) != 0

    @staticmethod
    def is_invalid_starter(card: int) -> bool:
        return (
            Uno.is_wildcard(card)
            or card & Card.V_PLUS_TWO
            or card & Card.V_SKIP
            or card & Card.V_REVERSE
        )

    @staticmethod
    def are_same_colour(card1: int, card2: int) -> bool:
        """Checks if two cards have the same colour flag bit set

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
        mask = ((1 << 18) - 1) & ~15
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

    def change_colour(self, colour: str) -> None:
        """Changes the colour without changing the top card, as needed when +4 and colour change
        cards are used

        args:
            None

        returns:
            The card with just the colour
        """
        print(f"Col: {colour}")
        if colour == "UNKNOWN":
            return Card.CL_RED
        col = f"CL_{colour[0].replace('R', 'RED').replace('G', 'GREEN').replace('Y', 'YELLOW').replace('B', 'BLUE')}"
        return Card[col]
    
    def get_player_data(self, player: str) -> dict:
        return {
            "num_cards": len(self.user_hands[player])
        }

    def get_client_data(self, player: str) -> dict:
        """For Uno, the player data that is needed for each individual client is:
        The current top of the discard pile (c_facing_card)
        And the player's current hand (c_hand)
        """
        current_colour = self.c_col_card.get_colour() if Uno.is_wildcard(self.get_top_card()) else self.get_top_card().get_colour()
        return {
            "current_player": self.get_player_id(self.current_player),
            "c_facing_card": str(self.get_top_card()),
            "c_hand": [str(card) for card in self.user_hands[player]],
            "c_player_data": {p: self.get_player_data(p) for p in self.players},
            "c_colour": current_colour,
            "c_reversed": self.reversed,
            "display_message": "",
            "winners": self.winners
        }
