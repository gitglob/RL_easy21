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
        # List of card values
        self.cards_values = list(range(1, 11))
        self.red_cards = [f"r{value}" for value in self.cards_values]
        self.black_cards = [f"b{value}" for value in self.cards_values]
        self.cards = self.red_cards + self.black_cards

    @property
    def all_cards(self):
        # Return red and black cards into a single list
        return self.cards

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
        self.sums = []
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
        self.sum += self.card.value
        self.sums.append(self.sum)
        self.actions.append('h')

    def hit(self):
        # Draw card
        self.card = Deck.draw_card()
        self.cards.append(self.card)
        self.actions.append('h')

        # Adjust sum based on value and color
        if self.card.color == "b":
            self.sum += self.card.value
        else:
            self.sum -= self.card.value

        # Keep partial sums
        self.sums.append(self.sum)

    def stick(self):
        self.actions.append('s')
        self.sums.append(self.sum)
        self._stick = True

    def reset(self):
        self.sum = 0
        self.sums = []
        self.card = None
        self.cards = []
        self.actions = []
        self._stick = False

class Player(Gambler):
    def __init__(self):
        super().__init__()
        self.sums = []

    def step(self, s: State=None, a: str=None) -> State:
        """Takes as input a state s, and an action a, and returns a sample of the 
        next state s′ (which may be terminal if the game is finished) and reward r."""

        if a == 'h':
            self.hit()
        elif a == 's':
            self.stick()

        new_state = State(s.d_first_card, self.sum)
            
        return new_state
    
class Dealer(Gambler):
    def __init__(self):
        super().__init__()

    def step(self):
        # Stick if in [17, 21]
        if self.sum >= 17 and self.sum <= 21:
            self.stick()
        else:
            self.hit()
