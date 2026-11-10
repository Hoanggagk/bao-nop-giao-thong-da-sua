# SIMULATION SETUP AND EXPERIMENTAL PARAMETERS

Proximal Policy Optimization is trained in simulation and then evaluated with fixed weights against Carrot-Following (CF) \[14\]. Both controllers use the same quadcopter model and waypoint trajectory. The test trials do not update the learned parameters.

1.  **Simulation Environment**

Training and evaluation use ProjectAirSim \[12\], which supplies the simulated vehicle dynamics and the state information used in the feedback loop. In the X-configuration quadcopter model, the central frame link is configured with a mass of 1.0 kg, and the four rotor positions are located symmetrically at $\pm 0.253$ m along the body axes. The propeller diameter is 0.2286 m, and the maximum rotor speed is approximately 6396 r/min. Opposing rotor pairs counter-rotate to balance reaction torque in the simulated configuration.

ProjectAirSim's built-in flight controller converts North–East–Down velocity commands into low-level actions. The same interface is used by both methods, so the comparison concerns high-level guidance rather than the internal stabilization loops. No wind, sensor noise, delay, or model uncertainty is explicitly introduced; the experiment therefore does not test disturbance rejection or transfer to a physical vehicle.

2.  **PPO Training Parameters**

Table I summarizes the reported training parameters. Training comprises 500,000 interaction steps. The 0.05-s control period and 400-step limit give a maximum episode duration of 20 s. An episode can end earlier after final completion or a terminating safety event.

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
| GAE parameter, $\lambda$ \[15\] | 0.95 |
| Clipping parameter, $\epsilon$ | 0.2 |
| Initial action standard deviation | 1.0 |
| Minimum action standard deviation | 0.1 |
| Action standard-deviation decay step | 0.01 |
| Action standard-deviation decay interval | 50 episodes |
| Number of neurons per hidden layer | 64 |
| Number of hidden layers in Actor/Critic | 2 |
| Activation function | Tanh |

3.  **Reference Method**

CF implements the Carrot Chasing principle in \[14\]. It selects a look-ahead carrot point on the reference path and directs the velocity command toward that point. As path progress changes, the point moves forward and provides a continuously changing local target (Fig. 3).

Let $p_{t}$ denote the current quadcopter position and $p_{c}$ the carrot-point position on the reference path. The carrot point is selected at a look-ahead distance $L = 0.5$ m ahead of the current progress position along the path. The direction vector from the quadcopter to the carrot point is then given by

$$
d_{c} = p_{c} - p_{t}
\tag{10}
$$

For reference-speed magnitude $v_{ref}$, the command direction points from the vehicle to the carrot point:

$$
v_{CF}=v_{ref}\frac{p_c-p_t}{\lVert p_c-p_t\rVert_2}
\tag{11}
$$

Equation (11) normalizes the displacement and scales the unit direction by $v_{ref}$, so the command direction changes with the local path geometry. The angle $\theta_e$ in Fig. 3 only illustrates the geometric relationship and is not an input to (11).

<img src="../assets/figures/figure_03.png" style="width:5.58873in;height:4.33283in" />

Fig. 3. CF geometry; $\theta_e$ is illustrative and is not used in (11).

The evaluation trajectory contains 40 helical waypoints with a radius of 1.5 m, and its North–East–Down $z$ coordinate changes from −2.0 to −4.0 m. CF uses $L=0.5$ m and $v_{ref}=1.5$ m/s in every trial.

Both methods use component-wise North–East–Down bounds of \[−3, 3\] m/s. CF nevertheless retains a 1.5-m/s reference magnitude, while the learned policy can produce independently bounded components. The shared hard bounds do not normalize the operating speeds, so completion time cannot isolate controller effects. The same geometric error calculation is used for both methods.

4.  **Evaluation Metrics**

Completion time describes the duration from the start of the evaluated waypoint interval to completion of the final waypoint. Root-mean-square error and mean absolute error describe the magnitude of geometric trajectory deviation. The root-mean-square measure gives greater weight to larger deviations because errors are squared before averaging, whereas the mean absolute measure provides the average deviation magnitude in the original unit.

Let $p_k$ be the vehicle position and $p_k^{ref}$ the closest point on the piecewise-linear path connecting the waypoints at sample $k$. The geometric error is $e_k=\lVert p_k-p_k^{ref}\rVert_2$. This definition measures the shortest spatial deviation from the waypoint trajectory, independently of which point a time-parameterized reference would occupy at the same instant. It therefore evaluates geometric waypoint trajectory tracking rather than synchronization with a timed reference. Over $M$ samples from the first to final waypoint, the measures are computed as

$$
\text{RMSE}=\sqrt{\frac{1}{M}\sum_{k=1}^{M}e_k^2},
\tag{12}
$$

and

$$
\text{MAE}=\frac{1}{M}\sum_{k=1}^{M}|e_k|,
\tag{13}
$$
