# Standard
import os
# External
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
# Local
from mc_functions import ActionValueFunctions


def plot_results(Qs: ActionValueFunctions, num_episodes: int):
    """Plots the optimal value functions in a 3D plot."""    
    # Extract the best action-value functions, along with the states
    # Basically, the best value function out of the 2, corresponding to the 2 possible actions
    best_qs = Qs.max()
    
    # Extract the xs, ys, zs for the 3d plot
    xs = np.arange(1, 11)
    ys = np.arange(1, 22)

    # Creating meshgrid
    X, Y = np.meshgrid(xs, ys)
    
    # Prepare the zs
    # In a surface plot, Z needs to be in the same shape as X and Y
    Z = best_qs.T

    # Draw the plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, antialiased=False)
    
    # Set axis titles
    ax.set_xlabel("Dealer's First Card")
    ax.set_ylabel("Player Sum")
    ax.set_title(f"Value Function - # Episodes: {num_episodes}")

    # Set axis limits
    ax.set_xlim(1, 10)
    ax.set_ylim(1, 21)
    ax.set_zlim(-1, 1)

    # Setting axis ticks
    ax.set_xticks(np.arange(1, 11, 1))
    ax.set_yticks(np.arange(1, 22, 1))
    ax.set_zticks(np.arange(-1, 1, 0.5))
    
    savepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", f"vf-plot-{num_episodes}.png")
    plt.savefig(savepath)
    plt.show()
    