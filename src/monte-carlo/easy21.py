# Standard
from typing import Tuple
# External
# Local
from definitions import Deck, State
from definitions import Player, Dealer


class Easy21():
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()

    @property
    def first_state(self) -> State:
        return State(self.dealer.cards[0], self.player.cards[0].value)

    @property
    def over(self) -> bool:
        c1 = self.player.busted
        c2 = self.player.sticked and self.dealer.busted
        c3 = self.player.sticked and self.dealer.sticked
        return True if c1 or c2 or c3 else False
        
    def start(self):
        # Reset players
        self.player.reset()
        self.dealer.reset()
        # Start
        self.dealer.start()    
        self.player.start()

    def step(self, s: State=None, a: str=None) -> Tuple[State, int]:
        """Takes as input a state s, and an action a, and returns a sample of the 
        next state s′ (which may be terminal if the game is finished) and reward r."""

        if a == 'h':
            self.player.hit()
        elif a == 's':
            self.player.stick()

        reward = self.decide_reward()
        new_state = State(self.dealer.cards[0], self.player.sum)
            
        return (new_state, reward)

    def decide_reward(self):
        """Decide winner of game."""
        if self.player.busted:
            reward = -1
        elif self.dealer.busted:
            reward = +1
        elif self.player.sticked and self.dealer.sticked:
            if self.dealer.sum > self.player.sum:
                reward = -1
            elif self.player.sum > self.dealer.sum:
                reward = +1
        else:
            reward = 0

        return reward
