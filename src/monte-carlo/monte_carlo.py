# Standard
import argparse
import time
# External
from numpy import mean
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

        # Initial state
        self.game.start()

        # Randomly initialize the state and action
        state = self.game.first_state

        # Run the game until it is over
        while not self.game.over:
            if self.game.whose_turn == 'p':
                # Get the number of state visits and the best action at this state
                state_count = self.H_s.get(state)
                greedy_action = self.Qs.argmax(state)

                # Decide an action based on the greedy policy
                action = greedy_policy(state_count, greedy_action)

                # Save the states, actions
                states.append(state)
                actions.append(action)

                # Player does 1 step and get possible reward
                state, reward = self.game.step(state, action)
                rewards.append(reward)
        
        # Return the list of states, actions, and rewards during this episode
        # print(f"Player {self.game.player.sum} vs. Dealer {self.game.dealer.sum}")
        return states, actions, rewards

    def run(self, num_episodes: int=1000, num_iter: int=1000):
        # Simulate X number of episodes
        start_time = time.time()
        prev_time = time.time()
        episode_lengths = []
        for i in range(num_episodes):
            # Run episode
            states, actions, rewards = self.simulate_episode()
            episode_lengths.append(len(actions))

            # Iterate over every state and action in he episode
            for state, action in zip(states, actions):
                # The reward of the first occurange of the state-action pair
                first_occurrence_idx = next(i for i,x in enumerate(zip(states, actions)) 
                                            if x[0] == state and x[1] == action)
                G = rewards[first_occurrence_idx]
                
                # Update state (s_counts, policies) and state-action (sa_counts, rewards) counts
                self.H_s.add(state)
                self.H_sa.add(state, action)

                # Update the action value functions
                N = self.H_sa.get(state, action)
                self.Qs.update(state, action, G, N)

            # For large runs, print out the progress intermittently
            if i % num_iter == 0:
                elapsed_time = time.time() - start_time
                print(f'Processed {i} episodes in {elapsed_time:.2f} sec...')
                avg_duration = (time.time() - prev_time) / num_iter
                print("\tAverage episode:"
                      f"\t\tduration: {avg_duration:.5f}"
                      f"\t\tlength: {mean(episode_lengths)}")
                prev_time = time.time()

        plot_results(self.Qs, num_episodes)


def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(description='Run the Monte Carlo simulation.')

    # Adding a positional argument
    parser.add_argument('episodes', 
                        type=int, 
                        nargs='?', 
                        help='Number of episodes to run', 
                        default=1000)

    # Parsing the arguments
    args = parser.parse_args()

    MC = MonteCarlo()
    MC.run(args.episodes)

if __name__ == "__main__":
    main()
