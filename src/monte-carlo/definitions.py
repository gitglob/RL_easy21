# Standard
from dataclasses import dataclass
from enum import Enum
import random
# External
# Local

      
class Card:
    """Represents a card in the deck"""
    value: int
    color: str

    def __str__(self):
        # Returning a string representation of the card
        return f"{self.color}{self.value}"

    def __repr__(self):
        # Custom representation for debugging
        return f"{self.color}{self.value}"

@dataclass
class State:
    """Dealer’s first card 1–10 and the player’s sum 1–21"""
    d_first_card: Card
    p_sum: int

    def __str__(self):
        return f"{self.d_first_card}-{self.p_sum}"

    def to_tuple(self):
        return (self.d_first_card, self.p_sum)

    def to_key(self):
        return (str(self.d_first_card), self.p_sum)
    
class Deck():
    def __init__(self):
        pass

    @property
    def all_cards(self):
        # List of card values
        card_values = list(range(1, 11))

        # Creating the list of cards
        red_cards = [f"r{value}" for value in card_values]
        black_cards = [f"b{value}" for value in card_values]

        # Return red and black cards into a single list
        return red_cards + black_cards

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
        card.color = "b"
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
        return "r" if color_prob < 1/3 else "b"
        
class Gambler():
    def __init__(self):
        self.sum = 0
        self.cards = []
        self.actions = []
        self.card = None
        self._stick = False

    @property
    def busted(self) -> bool:
        return True if self.sum < 1 or self.sum > 21 else False

    @property
    def sticked(self) -> bool:
        return True if self._stick else False

    @property
    def first_card(self) -> bool:
        return self.cards[0] if self.cards else None

    def start(self):
        self.card = Deck.draw_first_card()
        self.cards.append(self.card)
        self.actions.append('h')
        self.sum += self.card.value

    def hit(self):
        pass

    def stick(self):
        self.actions.append('s')
        self._stick = True

    def reset(self):
        self.sum = 0
        self.cards = []
        self.actions = []
        self.card = None
        self._stick = False

class Player(Gambler):
    def __init__(self, rl=False):
        self.rl = rl
        super().__init__()

    def hit(self):
        self.card = Deck.draw_card()
        self.cards.append(self.card)
        self.actions.append('h')

        if self.card.color == "b":
            self.sum += self.card.value
        else:
            self.sum -= self.card.value

class Dealer(Gambler):
    def __init__(self):
        super().__init__()

    def hit(self):
        self.card = Deck.draw_card()
        self.actions.append('h')
        self.cards.append(self.card)

        if self.card.color == "b":
            self.sum += self.card.value
        else:
            self.sum -= self.card.value

        if self.sum >= 17 and self.sum <= 21:
            self.stick()
