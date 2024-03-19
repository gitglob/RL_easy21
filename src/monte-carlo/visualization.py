# Standard
import os
# External
from matplotlib import pyplot as plt
import numpy as np
# Local
from definitions import Deck
from mc_functions import ActionValueFunctions


def plot_results(Qs: ActionValueFunctions):
    """Plots the optimal value functions in a 3D plot."""
    # Make a dictionary with all the possible states
    deck = Deck()
    
    # Extract the best action-value functions, along with the states
    # Basically, the best value function out of the 2, corresponding to the 2 possible actions
    best_qs = Qs.max()

    # Extract the xs, ys, zs for the 3d plot
    xs = np.arange(1, 11)
    ys = np.arange(1, 22)

    # Creating meshgrid
    X, Y = np.meshgrid(xs, ys)

    # Draw the plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(X, Y, best_qs)
    
    # Set axis titles
    ax.set_xlabel("Dealer's First Card")
    ax.set_ylabel("Player Sum")
    ax.set_zlabel("Value Function")

    # Set axis limits
    ax.set_xlim(1, 10)
    ax.set_ylim(1, 21)
    # ax.set_zlim(left=0)

    # Setting axis ticks
    ax.set_xticks(np.arange(1, 11, 1))
    ax.set_yticks(np.arange(1, 22, 1))
    
    savepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "vf-plot.png")
    plt.savefig(savepath)
    