# Description

The goal of this project is to apply reinforcement learning methods to the simple card game - Easy21.

This is the assignment from the RL course by David Silver - https://www.youtube.com/watch?v=2pWv7GOvuf0&list=PLzuuYNsE1EZAXYR4FJ75jcJseBmo4KQ9- .

# Conclusions

## Monte-Carlo
![Monte Carlo](/src/monte-carlo/results/vf-plot-1000000.png)
The Monte-Carlo method learns the value function from complete episodes of gameplay, averaging the returns after each visit to a state-action pair. The result is a direct estimate of the expected return from each state, giving us a value function that is specifically tailored to the sample of Easy21 games it has seen.

The plot for Monte-Carlo shows a clear division in value between certain state-action pairs, which indicates that the algorithm has learned from the episodic returns which states are generally favorable or unfavorable. As the plot suggests, the player's sum and the dealer's first card play a significant role in determining the value of each state.

For example, the value is higher when the dealer's first card is small, indicating that the dealer is more likely to bust, and it is lower when the player's sum is high, indicating a higher risk of busting. Since Monte-Carlo uses a lot of episodes, these patterns should be quite accurate representations of the value function for the policy being evaluated.

## TD-learning with Sarsa(λ)
### Lamda = 0
![Sarsa(0)](/src/TD-learning/results/vf-plot-10000-0.0.png)
With SARSA(λ) where λ = 0, the algorithm is myopic in its learning, focusing only on immediate rewards and not taking future rewards into account. This form of SARSA, also known as SARSA(0), does not consider the long-term consequences of actions, as there is no eligibility trace to carry the information forward through the episode.

In the context of Easy21, the only immediate reward occurs at the end of a hand, typically when the player wins, loses, or ties (pushes). Therefore, the value function is mostly flat because the immediate reward for all state-action pairs except from the terminal is zero. When the player gets a sum of 21, they win, hence the spike indicating a positive reward.

This plot underscores the importance of using a non-zero λ in SARSA(λ) for games where rewards are delayed until the end of the episode. A larger λ would allow the algorithm to account for future rewards by backpropagating the information from the terminal reward to previous states within the episode, leading to a more informed value function that better reflects the long-term outcomes of decisions.

### Lamda = 1
![Sarsa(1)](/src/TD-learning/results/vf-plot-10000-1.0.png)
In SARSA(λ) with λ=1, the value function displays a understanding of the state space, incorporating the long-term effects of the state-action pairs. The algorithm now credits all visited states within an episode, akin to Monte-Carlo methods, which results in a smoother and more strategic landscape of state values. This plot suggests a more accurate estimation compared to SARSA(0), as it reflects the cumulative impact of actions on eventual outcomes, essential in games with delayed rewards like Easy21.

### Lamda = 0.5
![Sarsa(0.5)](/src/TD-learning/results/vf-plot-10000-0.5.png)
The SARSA(λ) value function for λ=0.5 strikes a balance between the immediate and long-term rewards. This is evident by the smoother gradient of the value function.

## TD-learning with Sarsa(λ) and Linear Function Approximation
![Sarsa(0.5)](/src/lfa/results/vf-plot-10000-0.5.png)
SARSA(λ) with Linear Function Approximation reveals sharp peaks and troughs, which indicates overfitting to certain state-action pairs due to the coarse coding scheme. It suggests that the linear approximation overemphasized the values of some features while undervaluing others. The high peaks are a result of correlated updates across overlapping features (values 4 and 7 exist in 4 different player and dealer intervals each), leading to an exaggerated estimation of the state-action values. This emphasizes the need for careful tuning of feature representation or regularization to prevent overfitting.