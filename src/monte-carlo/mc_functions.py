# Standard
import random
# External
import numpy as np
# Local
from definitions import State, Deck


class StateHistory():
    """Stores state visits."""
    def __init__(self):
        deck = Deck()
        self.state_counts = {(card_id, p_sum): 0
                             for card_id in deck.all_cards
                             for p_sum in range(1, 22)}

    def add(self, s: State):
        """Increases the count of a state's visits."""
        self.state_counts[s.to_key()] += 1

    def get(self, s: State):
        """Returns the number of visits of a specific state."""
        return self.state_counts[s.to_key()]

class StateActionHistory():
    """Stores visits of state-action pairs."""
    def __init__(self):
        deck = Deck()
        self.state_counts = {(d_first_card_id, p_sum, action): 0
                             for d_first_card_id in deck.all_cards
                             for p_sum in range(1, 22)
                             for action in ['h', 's']}
        
    def add(self, s: State, a: str):
        """Increases the visit count of a State-Action pair."""
        self.state_counts[(str(s.d_first_card), s.p_sum, a)] += 1
        
    def get(self, s: State, a: str):
        """Returns the visit count of a State-Action pair."""
        return self.state_counts[(str(s.d_first_card), s.p_sum, a)]
        
class ActionValueFunctions():
    def __init__(self):
        deck = Deck()
        self.avfs = {(d_first_card_id, p_sum, action): 0
                     for d_first_card_id in deck.all_cards
                     for p_sum in range(1, 22)
                     for action in ['h', 's']}
        
    def add(self, s: State, a: str, G: int, N: int):
        """Increases the AVF value based on the episode score G and the count of
        the current state-action pairs N."""
        Q = self.avfs[(str(s.d_first_card), s.p_sum, a)]
        Q = Q + (1/N) * (G - Q)
        self.avfs[(str(s.d_first_card), s.p_sum, a)] = Q
        
    def get(self, s: State, a: str):
        """Returns the Action Value Function Q(s, a)"""
        return self.avfs[(str(s.d_first_card), s.p_sum, a)]
    
    def argmax(self, s: State) -> str:
        """Returns the Action that maximizes Q in the current state"""
        # Extracting the sub-dictionary for the current state
        state_avfs = {action: q_value 
                    for (d_first_card_id, p_sum, action), q_value in self.avfs.items()
                    if d_first_card_id == str(s.d_first_card) and p_sum == s.p_sum}
        
        # Finding the action that maximizes the Q value
        greedy_action = max(state_avfs, key=state_avfs.get)
        
        return greedy_action
    
    def max(self) -> str:
        """
        Returns the best Action Value Functions for every state.
        
        Basically, picks the highest Q out of the 2 possible actions for every state.
        """
        # Initialize a 3D NumPy array
        q_values_array = np.zeros((10, 21, 2)) # 10 21 2

        # Populate the 4D array
        for (d_first_card_id, p_sum, action), q_value in self.avfs.items():
            card_index = int(str(d_first_card_id)[1:]) - 1  # Convert card 'b1'...'b10' to 0...9
            p_sum_index = p_sum - 1  # Convert p_sum 1...21 to 0...20
            action_index = 0 if action == 'h' else 1  # Convert action 'h'/'s' to 0/1
            q_values_array[card_index, p_sum_index, action_index] = q_value

        # Find the best action for each (d_first_card_id, p_sum) pair
        best_actions_q_values = np.max(q_values_array, axis=2) # 10 21

        # All_q_values now contains your original q_values plus the best q_values in the last slice of the third dimension
        return best_actions_q_values
    
def greedy_policy(N_s, a_star, N0=100):
    """
    e-Greedy Exploration implementation, where N_s is the number of
    times a state has been visited, and a_star is the optimal action.
    
    The lower N0 is, the less exploration we do, and the faster we
    we converge to basically always selecting the greedy, best action.
    """
    e = N0 / (N0 + N_s)  # Exploration rate
    prob = e / 2 + 1 - e  # Probability of choosing the optimal action

    explore_action = 's' if a_star == 'h' else 'h'
        
    return a_star if random.random() < prob else explore_action
