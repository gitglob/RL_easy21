# Standard
from dataclasses import dataclass
from enum import Enum
import random
# External
# Local


class Color(Enum):
    RED = "red"
    BLACK = "black"

class Action(Enum):
    """Player action (hit or stick)"""
    HIT = "hit"
    STICK = "stick"

class Card:
    """Represents a card in the deck"""
    value: int
    color: Color

    def __str__(self):
        # Returning a string representation of the card
        return f"({self.value} , {self.color})"

    def __repr__(self):
        # Custom representation for debugging
        return f"({self.value} , {self.color})"
        
@dataclass
class State:
    """Dealer’s first card 1–10 and the player’s sum 1–21"""
    d_first_card: Card
    p_sum: int

class Deck():
    def __init__(self):
        pass

    @staticmethod
    def draw_card():
        card = Card()
        card.value = Deck.get_value()
        card.color = Deck.get_color()
        return card

    @staticmethod
    def draw_first_card():
        card = Card()
        card.value = Deck.get_value()
        card.color = "black"
        return card

    @staticmethod
    def get_value():
        # Each draw results in a value 1-10
        card = random.randint(1, 10)
        return card

    @staticmethod
    def get_color():
        # Generate a random number between 0 and 1
        color_prob = random.random()
        # Assign color based on the probabilities red: 1/3, black: 2/3
        return "red" if color_prob < 1/3 else "black"
        
class Gambler():
    def __init__(self):
        self.sum = 0
        self.cards = []
        self.actions = []
        self.card = None
        self._stick = False

    @property
    def busted(self) -> bool:
        if self.sum < 1 or self.sum > 21:
            return True
        else:
            return False

    @property
    def sticked(self) -> bool:
        return True if self._stick else False

    @property
    def first_card(self) -> bool:
        if self.cards:
            return self.cards[0]
        else:
            return None

    def play(self):
        while not self.busted and not self.sticked:
            self.hit()
            self.log_status()

    def start(self):
        self.card = Deck.draw_first_card()
        self.cards.append(self.card)
        self.actions.append(Action.HIT)
        self.sum += self.card.value
        self.log_status()

    def hit(self):
        pass

    def stick(self):
        self.actions.append(Action.STICK)
        self._stick = True

    def reset(self):
        self.sum = 0
        self.cards = None
        self.actions = None
        self.card = None
        self._stick = False

    def log_status(self):
        print(f"Hit card: {self.card}\n"
               "---------------------\n"
              f"Cards:    {self.cards}\n"
              f"Actions:  {[a.value for a in self.actions]}\n"
              f"Sum:      {self.sum}\n"
               "---------------------\n"
              f"Sticked:  {self.sticked}\n"
              f"Busted:   {self.busted}\n")

class Player(Gambler):
    def __init__(self):
        super().__init__()

    def hit(self):
        self.card = Deck.draw_card()
        self.cards.append(self.card)
        self.actions.append(Action.HIT)

        if self.card.color == "black":
            self.sum += self.card.value
        else:
            self.sum -= self.card.value

        if self.sum >= 15 and self.sum <= 21:
            self.stick()

class Dealer(Gambler):
    def __init__(self):
        super().__init__()

    def hit(self):
        self.card = Deck.draw_card()
        self.actions.append(Action.HIT)
        self.cards.append(self.card)

        if self.card.color == "black":
            self.sum += self.card.value
        else:
            self.sum -= self.card.value

        if self.sum >= 17 and self.sum <= 21:
            self.stick()
