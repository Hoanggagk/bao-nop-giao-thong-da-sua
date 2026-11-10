Table I. PPO training parameters

| **Parameter** | **Value** |
|:--|:--|
| Total training timesteps | 500,000 |
| Maximum timesteps per episode | 400 |
| Control period, $\Delta t$ | 0.05 s |
| PPO update interval | 2000 timesteps |
| Actor learning rate | $3 \times 10^{- 4}$ |
| Critic learning rate | $1 \times 10^{- 3}$ |
| Number of update epochs, K | 5 |
| Discount factor, $\gamma$ | 0.99 |
| GAE parameter, $\lambda$ \[25\] | 0.95 |
| Clipping parameter, $\epsilon$ | 0.2 |
| Initial action standard deviation | 1.0 |
| Minimum action standard deviation | 0.1 |
| Action standard-deviation decay step | 0.01 |
| Action standard-deviation decay interval | 50 episodes |
| Number of neurons per hidden layer | 64 |
| Number of hidden layers in Actor/Critic | 2 |
| Activation function | Tanh |
