# Standard
import random
# External
import numpy as np
# Local
from definitions import State, Deck, Card


class EligibilityTraces():
    def __init__(self, gamma, lamda):
        self.gamma = gamma
        self.lamda = lamda

        # Parameter vector
        self.Es = np.zeros(36)
        
    def update(self, gradQ):
        """Updates the Eligibility Traces based on the weight gradient,
        the discount factor, and the eligibility trace decay rate."""
        self.Es = self.gamma * self.lamda * self.Es + gradQ

    def get(self):
        return self.Es
        
class FeatureVector():
    def __init__(self, alpha):
        self.alpha = alpha

        # Linear Function Approximation intervals
        self.dealer_intervals = [(1, 4), (4, 7), (7, 10)]
        self.player_intervals = [(1, 6), (4, 9), (7, 12), (10, 15), (13, 18), (16, 21)]
        self.actions = ['h', 's']

        # Parameter vector
        self.theta = np.zeros(len(self.dealer_intervals)
                              * len(self.player_intervals)
                              * len(self.actions))
        
    def get(self, s: State, a: str):
        """Generate the feature vector for a given state and action"""
        dealer_card = s.d_first_card.value
        player_sum = s.p_sum

        feature = np.zeros((len(self.dealer_intervals), 
                            len(self.player_intervals),
                            len(self.actions)))
        
        for i, (d_start, d_end) in enumerate(self.dealer_intervals):
            for j, (p_start, p_end) in enumerate(self.player_intervals):
                for k, act in enumerate(self.actions):
                    if d_start <= dealer_card <= d_end and p_start <= player_sum <= p_end and a == act:
                        feature[i, j, k] = 1

        return feature.flatten()
    
    def get_Q(self, s: State, a: str):
        """Returns the Action Value Function for a specific state-action pair."""
        phi = self.get(s, a)
        return np.dot(phi, self.theta)
    
    def get_gradQ(self, s: State, a: str):
        """Returns the gradient of the Action Value Function for a specific state-action pair."""
        phi = self.get(s, a)
        return phi
            
    def update(self, s: State, a: str, delta: float, Es: EligibilityTraces):
        """Update the weight vector based on the td error, the eligibility traces,
        and the feature vector for this specific state-action pair."""
        self.theta = self.theta + self.alpha * delta * Es.get() * self.get(s, a)
      
    def argmax(self, s: State) -> str:
        """Returns the Action that maximizes Q in the current state"""
        # Get the AVFs
        Q_values = [self.get_Q(s, action) for action in self.actions]

        # Finding the action that maximizes the Q value
        greedy_action = self.actions[np.argmax(Q_values)]
        
        return greedy_action

    @staticmethod
    def find_interval_indices(value: int, intervals: list):
        """Finds the index of the interval a value fits in, given a list of intervals."""
        return [index for index, interval in enumerate(intervals) if interval[0] <= value <= interval[1]]

    @staticmethod
    def cardID2card(card_id: str):
        """Convert the card ID to a card."""
        card = Card()
        card.value = int(card_id[1])
        card.color = card_id[0]
        return card

    def max(self) -> np.ndarray:
        """
        Returns the best Action Value Functions for every state.
        
        Basically, picks the highest Q out of the 2 possible actions for every state.
        """
        # Calculate the AVF for all possible states
        deck = Deck()
        avfs = {(d_first_card_id, p_sum, action): 
                    self.get_Q(State(self.cardID2card(d_first_card_id), p_sum), action)
                for d_first_card_id in deck.all_cards
                for p_sum in range(1, 22)
                for action in ['h', 's']}
        
        # Initialize a 3D NumPy array
        q_values_array = np.zeros((10, 21, 2)) # 10 21 2

        # Populate the 4D array
        for (d_first_card_id, p_sum, action), q_value in avfs.items():
            card_index = int(str(d_first_card_id)[1:]) - 1  # Convert card 'b1'...'b10' to 0...9
            p_sum_index = p_sum - 1  # Convert p_sum 1...21 to 0...20
            action_index = 0 if action == 'h' else 1  # Convert action 'h'/'s' to 0/1
            q_values_array[card_index, p_sum_index, action_index] = q_value

        # Find the best action for each (d_first_card_id, p_sum) pair
        best_actions_q_values = np.max(q_values_array, axis=2) # 10 21

        # All_q_values now contains your original q_values plus the best q_values in the last slice of the third dimension
        return best_actions_q_values
    
def greedy_policy(a_star, e=0.05):
    """
    e-Greedy Exploration implementation.
    
    Args:
        a_star (str): The optimal action ('h' for hit, 's' for stick)
        e (float): Exploration probability (default 0.05)
    """
    prob = e / 2 + 1 - e  # Probability of choosing the optimal action

    explore_action = 's' if a_star == 'h' else 'h'
        
    return a_star if random.random() < prob else explore_action

def td_error(reward, Q, Q_next, gamma):
    delta = reward + gamma*Q_next - Q
    return delta
