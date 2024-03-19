# Standard
import random
# External
# Local
from easy21 import Easy21
from mc_functions import StateHistory, StateActionHistory, ActionValueFunctions, greedy_policy
from visualization import plot_results

   
class MonteCarlo():
    def __init__(self):
        self.game = Easy21()

        # Initialize state and state-action history
        self.H_s = StateHistory()
        self.H_sa = StateActionHistory()
        self.Qs = ActionValueFunctions()

    def simulate_episode(self):
        """Simulates a full Easy21 episode."""
        states = []
        actions = []
        rewards = []

        # Initial reward
        reward = 0

        # Randomly initialize the state and action
        state = self.game.first_state
        action = 'h'

        # Run the game until it is over
        while not self.game.over:
            # Get the number of state visits and the best action at this state
            state_count = self.H_s.get(state)
            greedy_action = self.Qs.argmax(state)

            # Decide an action based on the greedy policy
            action = greedy_policy(state_count, greedy_action)

            # Save the states, actions, rewards
            states.append(state)
            actions.append(action)
            rewards.append(reward)

            # Do 1 step in the game
            state, reward = self.game.step(state, action)
        
        # Return the list of states, actions, and rewards during this episode
        return states, actions, rewards

    def run(self):
        # Simulate X number of episodes
        num_episodes = 10000
        for i in range(num_episodes):    
            # Initial state
            self.game.start()

            # Run episode
            states, actions, rewards = self.simulate_episode()

            # Iterate over every state and action in he episode
            for state, action in zip(states, actions):
                # The reward of the first occurange of the state-action pair
                first_occurrence_idx = next(i for i,x in enumerate(zip(states, actions)) 
                                            if x[0] == state and x[1] == action)
                G = rewards[first_occurrence_idx]
                
                # Update state (s_counts, policies) and state-action (sa_counts, rewards) history
                self.H_s.add(state)
                self.H_sa.add(state, action)
                self.Qs.add(state, action, G, self.H_sa.get(state, action))

            # For large runs, print out the progress intermittently
            if i % 100 == 0:
                print(f'Processed {i} episodes...')

        plot_results(self.Qs)


def main():
    MC = MonteCarlo()
    MC.run()

if __name__ == "__main__":
    main()
