# Standard
from typing import Tuple, Literal
# External
# Local
from definitions import Deck, State
from definitions import Player, Dealer, Gambler


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
    
    @property
    def whose_turn(self) -> Gambler:
        return self.turn
        
    def start(self):
        # Restart game
        self.player.reset()
        self.dealer.reset()
        self.player.start()
        self.dealer.start()
        self.turn = 'p'

    def player_step(self, s, a):
        if a == 's':
            self.turn = 'd'
        return self.player.step(s, a)


    def dealer_step(self):
        self.dealer.step()

    def decide_rewards(self):
        """Decide rewards for an episode."""
        rewards = []

        # Iterate over every player sum
        for player_sum in self.player.sums:
            if player_sum < 1 or player_sum > 21:
                reward = -1
            elif self.dealer.busted:
                reward = +1
            else:
                if self.dealer.sum > player_sum:
                    reward = -1
                elif player_sum > self.dealer.sum:
                    reward = +1
                else:
                    reward = 0

            rewards.append(reward)

        return rewards
