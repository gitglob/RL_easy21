# Standard
from typing import Literal
# External
# Local
from definitions import Deck, State
from definitions import Player, Dealer


class Easy21():
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()
        self.turn: Literal['p', 'd'] = None

    @property
    def first_state(self) -> State:
        return State(self.dealer.cards[0], self.player.cards[0].value)

    @property
    def over(self) -> bool:
        c1 = self.player.busted
        c2 = self.player.sticked and (self.dealer.sum > self.player.sum)
        c3 = self.player.sticked and self.dealer.busted
        c4 = self.player.sticked and self.dealer.sticked
        return True if c1 or c2 or c3 or c4 else False
        
    def start(self):
        # Restart game
        self.player.reset()
        self.dealer.reset()
        self.player.start()
        self.dealer.start()

    def step(self, s, a):
        new_state = self.player.step(s, a)
        if a == 's':
            while not self.over:
                self.dealer.step()

        reward = self.decide_reward()
        
        return new_state, reward

    def decide_reward(self):
        """Decide reward for a step of an episode."""
        if self.player.sum < 1 or self.player.sum > 21:
            reward = -1
        elif self.dealer.busted:
            reward = +1
        else:
            if self.dealer.sum > self.player.sum:
                reward = -1
            elif self.player.sum > self.dealer.sum:
                reward = +1
            else:
                reward = 0

        return reward
