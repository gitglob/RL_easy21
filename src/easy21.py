# Standard
from typing import Tuple
# External
# Local
from definitions import Deck, State, Action
from definitions import Player, Dealer


class Easy21():
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()

    def start(self):
        print("\t\t\t\t\tDealer draws first card")
        self.dealer.start()    
        print("\t\t\t\t\tPlayer draws first card")
        self.player.start()

    def step(self, s: State=None, a: Action=None) -> Tuple[State, int]:
        """Takes as input a state s, and an action a, and returns a sample of the 
        next state s′ (which may be terminal if the game is finished) and reward r."""
        dealer_card, player_sum = s
        
        if a == Action.HIT:
            # Draw card
            reward = self.player.hit()
        elif a == Action.STICK:
            reward = self.player.stick()
            
        return ((self.dealer.cards[0], self.player.sum), reward)

    def finish(self):
        """Decide winner of game."""
        print(f"Player: Sum: {self.player.sum}")
        print(f"Dealer: Sum: {self.dealer.sum}")

        if self.player.busted:
            winner = "dealer"
        elif self.dealer.busted:
            winner = "player"
        elif self.dealer.sum > self.player.sum:
            winner = "dealer"
        elif self.dealer.sum < self.player.sum:
            winner = "player"
        else:
            winner = "None"

        print(f"Winner: {winner}")

        if winner == "player":
            reward = 1
        elif winner == "dealer":
            reward = -1
        else:
            reward = 0

        print(f"Reward: {reward}")

        return reward
    
    def reset(self):
        "Starts new game"
        self.player.reset()
        self.dealer.reset()
        
    def play(self):
        """
        Play one round.
        
        1. Both player and dealer draw 1 card
        2. Player draws as much as they want
        3. Dealer draws until 17+ or bust
        4. Winner is decided
        5. Game is reset
        """
        # 1. Game starts
        print("\t\t\t\t\tGame starts")
        self.start()

        # 2. Player draws
        print("\t\t\t\t\tPlayer's turn")
        self.player.play()

        # 3. Dealer draws
        if not self.player.busted:
            print("\t\t\t\t\tDealer's turn")
            self.dealer.play()

        # 4. Winner is decided
        print("\t\t\t\t\tGame finished")
        winner = self.finish()

        # 4. Winner is decided
        self.reset()

        return winner