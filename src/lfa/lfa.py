# Standard
import argparse
import time
# External
# Local
from easy21 import Easy21
from lfa_functions import EligibilityTraces, FeatureVector
from lfa_functions import td_error, greedy_policy
from visualization import plot_results

   
class LFA():
    def __init__(self, gamma: float=0.98, lamda: float=0.5, alpha: float=0.01):
        self.game = Easy21()

        # Initialize parameters
        self.gamma = gamma # Discount factor
        self.lamda = lamda # Eligibility trace decay rate
        self.alpha = alpha # Learning rate

        # Initialize state and state-action history
        self.Es = EligibilityTraces(gamma, lamda)
        self.FV = FeatureVector(alpha)

    def run(self, 
            num_episodes: int=1000, 
            num_iter: int=1000):
        """
        Runs TD-Learning with Sarsa(lamda).
        
        num_episodes: number of episodes to run
        num_iter: logging period (log every X number of iteratios)
        gamma: discount factor
        """
        # Simulate X number of episodes
        start_time = time.time()
        prev_time = time.time()
        for i in range(num_episodes):
            # Initial state
            self.game.start()

            # Randomly initialize the state and action
            state = self.game.first_state
            action = greedy_policy(self.FV.argmax(state))

            # Run the game until it is over
            while not self.game.over:
                # Get the best action at this state
                greedy_action = self.FV.argmax(state)

                # Decide an action based on the greedy policy
                new_action = greedy_policy(greedy_action)

                # 1 game step and get reward
                new_state, reward = self.game.step(state, action)

                # Get TD-error
                Q = self.FV.get_Q(state, action)
                new_Q = self.FV.get_Q(new_state, new_action)
                delta = td_error(reward, Q, new_Q, self.gamma)

                # Update eligibility trace
                self.Es.update(self.FV.get_gradQ(state, action))

                # Update parameter vector
                self.FV.update(state, action, delta, self.Es)

                # Update state and action
                state = new_state
                action = new_action

            # For large runs, print out the progress intermittently
            if i % num_iter == 0:
                elapsed_time = time.time() - start_time
                print(f'Processed {i} episodes in {elapsed_time:.2f} sec...')
                avg_duration = (time.time() - prev_time) / num_iter
                print(f"\tAverage episode duration: {avg_duration:.5f}")
                prev_time = time.time()

        plot_results(self.FV, num_episodes, self.lamda)


def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(description='Run the Sarsa(lamda) with Linear Function Approximation simulation.')

    # Adding a positional argument
    parser.add_argument('episodes', 
                        type=int, 
                        nargs='?', 
                        help='Number of episodes to run', 
                        default=1000)
                        
    parser.add_argument('lamda', 
                        type=float, 
                        nargs='?', 
                        help='Eligibility trace decay rate', 
                        default=0.5)

    # Parsing the arguments
    args = parser.parse_args()

    lfa = LFA(lamda=args.lamda)
    lfa.run(args.episodes)

if __name__ == "__main__":
    main()
