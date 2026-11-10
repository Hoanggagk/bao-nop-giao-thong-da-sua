<div align="center">

<img src="assets/figures/journal_logo.png" alt="Journal logo" width="64" />

**Transport and Communications Science Journal**

<img src="assets/figures/utc_logo.jpeg" alt="University logo" width="53" />

# WAYPOINT TRAJECTORY TRACKING CONTROL OF A QUADCOPTER USING PROXIMAL POLICY OPTIMIZATION

**Pham Thi Ly<sup>1</sup>, Nguyen Vinh Hoang<sup>1</sup>**

<sup>1</sup>University of Transport and Communications, No 3 Cau Giay Street, Hanoi, Vietnam

</div>

## ARTICLE INFO

TYPE: Research Article
Received: … (edited by editors)
Revised: … (edited by editors)
Accepted: … (edited by editors)
Published online: … (edited by editors)
https://doi.org/10.1080/14680629.2017.1389072 (edited by editors)

* Corresponding author
Email:vinhhoang2001k60@gmail.com; Tel: 0349418809 (optional)

*@ 2026 University of Transport and Communications*

# Abstract

This study investigates Proximal Policy Optimization for waypoint trajectory tracking control of a quadcopter in ProjectAirSim. The learned Actor–Critic policy uses vehicle motion and attitude together with relative errors to the current and next waypoints to generate velocity commands along the North–East–Down axes, while the built-in flight controller provides low-level stabilization. The reward combines waypoint completion, safety, target approach, and velocity alignment. After training, the fixed policy was evaluated against Carrot-Following on a helical waypoint trajectory. Both controllers completed the prescribed waypoint sequence. Proximal Policy Optimization maintained smaller geometric deviations from the waypoint trajectory and completed the task sooner under the tested configurations, although it produced larger roll and pitch variations during changes of direction. The completion-time difference should not be interpreted as an intrinsic advantage because the controller operating speeds were not normalized and the training objective encouraged early completion. Repeated evaluations characterize fixed-controller behavior rather than variation across independent training runs. The findings support the feasibility of learned high-level velocity control for the investigated waypoint trajectory tracking task. They do not establish general superiority, robustness, or real-world effectiveness because the evaluation used one trajectory without explicit disturbances, model uncertainty, or hardware experiments.

**Keywords:** Quadcopter, waypoint trajectory tracking, trajectory tracking control, Proximal Policy Optimization, reinforcement learning, Carrot-Following.

# 1. INTRODUCTION

Quadcopters are used in tasks such as infrastructure inspection and search-and-rescue operations \[1\], \[2\]. In these applications, autonomous flight may require the vehicle to pass through an ordered set of locations while remaining close to a prescribed trajectory. Reliable waypoint trajectory tracking control is challenging because quadcopters have nonlinear, coupled, and underactuated dynamics \[3\]. Translational motion is produced through changes in attitude and thrust, so a command intended to change motion along one direction can also affect other components of the vehicle response. A waypoint trajectory-tracking controller must therefore coordinate progression toward successive waypoints with the attitude changes required to realize three-dimensional motion.

Model-based and conventional control methods remain important approaches to quadcopter trajectory tracking. Published studies have addressed proportional–integral–derivative control \[4\], model predictive control \[5\], and robust sliding-mode control \[6\]. These methods can provide effective tracking when their models, structures, and parameters are suitable for the vehicle and operating conditions. Their implementation may nevertheless require a model or a controller-design and tuning process adapted to the system. Deep reinforcement learning offers a complementary formulation in which a policy is optimized through interaction with an environment. This formulation does not eliminate design dependence: policy behavior is still shaped by the simulator, observation and action spaces, reward, low-level controller, and training conditions.

Recent quadcopter studies have evaluated model-free reinforcement-learning algorithms for attitude control and trajectory tracking \[7\], examined real-time deep-reinforcement-learning control \[8\], applied Deep Deterministic Policy Gradient to trajectory tracking \[9\], and investigated Soft Actor–Critic for position control \[10\]. These studies show that continuous-control reinforcement learning is relevant to quadcopter guidance and stabilization, while also illustrating that the learned task depends on the selected algorithm and control formulation. Proximal Policy Optimization provides an Actor–Critic approach in which policy updates are constrained by a clipped surrogate objective \[11\]. Motivated by this literature, the present study examines Proximal Policy Optimization as a high-level velocity controller for waypoint trajectory tracking. The study does not claim novelty for the optimization algorithm or for hierarchical flight control itself.

The investigated formulation addresses three connected design requirements. First, the observation must identify the immediate target while representing how the trajectory continues beyond it. The state therefore contains relative errors to both the current and next waypoints in addition to vehicle motion and attitude variables. Second, waypoint completion alone would provide feedback only at discrete events. The reward consequently combines completion and safety terms with stepwise approach and velocity-alignment terms. Third, directly learning rotor-level stabilization would broaden the learning problem beyond waypoint guidance. The policy instead generates North–East–Down velocity commands, while the built-in flight controller executes the low-level stabilization and actuation required by those commands.

The resulting controller uses a fifteen-dimensional state and produces three continuous velocity-command components. Training is conducted in ProjectAirSim, after which the learned weights are fixed for evaluation. Carrot-Following is implemented as a reference guidance method on the same helical waypoint trajectory. The comparison uses completion time and geometric trajectory-deviation errors, together with trajectory, position, and attitude responses. Because the two controller configurations do not use the same velocity-magnitude specification, the completion-time result is interpreted as a property of the tested configurations rather than as an intrinsic speed advantage of Proximal Policy Optimization.

The study makes three contributions. First, it specifies a hierarchical control formulation for waypoint trajectory tracking in which current- and next-waypoint errors are combined with vehicle motion and attitude in the policy state, while the policy outputs velocity commands in the North–East–Down frame (Sections 2 and 3). Second, it defines a four-part reward for waypoint completion, unsafe termination, target approach, and velocity alignment, while avoiding claims about the isolated effect of any component because no reward ablation is available (Section 3). Third, it reports ten repeated evaluations of the fixed learned policy and Carrot-Following on one helical trajectory and interprets the error, timing, and attitude results within the limits of the experimental design (Sections 4 and 5).

The evidence is restricted to one ProjectAirSim trajectory, one fixed set of learned weights, and nominal simulation conditions without explicitly introduced wind, sensor noise, delay, or model uncertainty. The study includes neither hardware experiments nor evaluations across independent training seeds. Its findings therefore support feasibility under the tested conditions but do not establish general superiority, robustness, or real-world effectiveness.

# 2. WAYPOINT TRAJECTORY TRACKING PROBLEM

The control objective is to guide the quadcopter sequentially through the waypoint set $W = \{w_{1},\ldots,w_{N}\}$ in three-dimensional space, as illustrated in Fig. 1. The $i$th waypoint is $w_{i} = [x_{i},y_{i},z_{i}]^{T}$, and the position at control instant $t$ is $p_{t} = [x_{t},y_{t},z_{t}]^{T}$. Both are expressed in the inertial North–East–Down frame. The task is not merely to reach the final location, but to complete the intermediate targets in their prescribed order.

<img src="assets/figures/figure_01.png" style="width:6.11501in;height:2.33333in" />

Fig. 1. Waypoint trajectory tracking control problem for the quadcopter.

Two coordinate frames describe the motion. The inertial frame $\{I\}$ defines global position, where $X_I$, $Y_I$, and $Z_I$ correspond to North, East, and Down. The body-fixed frame $\{B\}$ is attached to the quadcopter and contains $x_B$, $y_B$, and $z_B$. Vehicle attitude relates the moving frame to the inertial frame, while the waypoints and translational-velocity commands use North–East–Down coordinates.

At each control instant, one waypoint $w_i$ is designated as the current target. The relative position between the quadcopter and this target provides the immediate direction and distance information used by the policy. When the waypoint-completion condition is satisfied, the target index advances from $i$ to $i+1$. This switching process continues until the final waypoint $w_N$ has been reached. The next waypoint is also included in the policy state so that the observation contains information about the local continuation of the trajectory rather than only the current point target.

Under this formulation, a successful controller must satisfy several objectives simultaneously. It must complete the waypoint sequence without triggering the stated termination conditions, remain close to the piecewise-linear path defined by the waypoints, and complete the task within the episode duration. These objectives are related but not identical: a controller can reach every waypoint while deviating between them, and a shorter completion time can be produced by a higher operating speed rather than by a better guidance law. For this reason, the experimental evaluation reports completion time together with geometric trajectory-deviation measures and interprets timing in light of the velocity settings used by each method.

# PPO-BASED CONTROLLER DESIGN

Fig. 2 shows the hierarchical architecture used in this study. Proximal Policy Optimization maps vehicle-state and waypoint information to velocity commands in the North–East–Down frame, and ProjectAirSim's low-level flight controller executes these commands \[12\]. The learned policy therefore determines the desired translational motion but does not replace the inner stabilization loops. Position, linear velocity, Euler angles, and angular velocity are returned at the next control instant to close the feedback loop. This division of responsibility makes the policy output directly comparable with the velocity command used by the reference method while retaining the simulator's established mechanism for converting desired motion into vehicle-level actuation.

<img src="assets/figures/figure_02.png" style="width:4.90639in;height:2.45833in" />

Fig. 2. Control architecture for quadcopter waypoint trajectory tracking.

## State Space Design

The state combines trajectory geometry, translational motion, and attitude. The current-waypoint error defines the immediate target, whereas the next-waypoint error represents the local continuation of the trajectory. Including both errors allows the observation to distinguish between vehicle states that may have a similar distance to the current waypoint but lead toward different subsequent segments. The remaining variables describe the motion and orientation with which the vehicle is approaching that local geometry. The resulting fifteen-dimensional state is

$$
s_{t} = \left\lbrack d_{x}^{i},d_{y}^{i},d_{z}^{i},d_{x}^{i + 1},d_{y}^{i + 1},d_{z}^{i + 1},v_{x},v_{y},v_{z},\phi,\theta,\psi,\dot{\phi},\dot{\theta},\dot{\psi} \right\rbrack^{\text{T}}
\tag{1}
$$

where:

- $d_{x}^{i},d_{y}^{i},d_{z}^{i}$ are the NED components of the relative error to waypoint $i$, defined by

$$
d_{i} = w_{i} - p_{t}
\tag{2}
$$

where $p_t=[x,y,z]^T\in\mathbb{R}^3$ is the quadcopter position and $w_i=[x_w,y_w,z_w]^T\in\mathbb{R}^3$ is waypoint $i$;

- $d_{x}^{i+1},d_{y}^{i+1},d_{z}^{i+1}$ are the error components to waypoint $i+1$ and provide information about the trajectory beyond the current target;

- $v_x,v_y,v_z$ are the NED linear-velocity components;

- $\phi,\theta,\psi$ are roll, pitch, and yaw;

- $\dot{\phi},\dot{\theta},\dot{\psi}$ are the corresponding angular velocities.

All position errors and linear velocities in (1) use the same inertial coordinates as the waypoints and actions. The attitude terms add the vehicle's rotational condition. The effect of the next-waypoint inputs is not isolated; it would require an otherwise identical policy trained without them.

## Action Space Design

Proximal Policy Optimization provides high-level velocity guidance while the ProjectAirSim flight controller stabilizes the vehicle. A three-dimensional continuous action is used because trajectory progression requires simultaneous motion in the North, East, and Down directions. The action at time $t$ is

$$
a_{t} = \left\lbrack v_{N}^{\text{cmd}},v_{E}^{\text{cmd}},v_{D}^{\text{cmd}} \right\rbrack^{\text{T}}
\tag{3}
$$

where $v_N^{\text{cmd}},v_E^{\text{cmd}},v_D^{\text{cmd}}$ are the North, East, and Down commands. PPO does not command thrust, moments, or rotor speeds; ProjectAirSim converts its velocity commands into low-level actions. Each component is constrained by

$$
v_{N}^{\text{cmd}},v_{E}^{\text{cmd}},v_{D}^{\text{cmd}} \in \lbrack - 3.0,3.0\rbrack\,\text{m/s}
\tag{4}
$$

The Gymnasium Box space \[13\] defines these component-wise action bounds during training and testing. The bounds restrict each coordinate but do not impose a fixed magnitude on the three-dimensional velocity vector, a distinction relevant to comparison with Carrot-Following. Lock-step interaction uses $\Delta t=0.05$ s, corresponding to 20 Hz.

## Reward Function Design

The reward combines completion and safety terms with dense approach and velocity-alignment feedback. A completion-only reward would be received at relatively few instants, whereas the two dense terms provide a stepwise indication of whether the motion is progressing toward the current target. The complete reward is

$$
R_{sum} = r_{waypoint} + r_{penalty} + r_{approach} + r_{align}
\tag{5}
$$

where:

- $R_{\text{sum}}$ is the reward at time $t$;

- $r_{\text{waypoint}}$ and $r_{\text{penalty}}$ represent completion and safety violation;

- $r_{\text{approach}}$ rewards decreasing target distance;

- $r_{\text{align}}$ rewards velocity directed toward the target.

**Waypoint-Completion Reward**

The completion reward is

$$
r_{waypoint}=\begin{cases}
10, & d(p_t,w_i)<r_w\text{ and }i<N,\\
15+15\dfrac{T_{\max}-t}{T_{\max}}, & d(p_t,w_i)<r_w\text{ and }i=N,\\
0, & \text{otherwise}.
\end{cases}
\tag{6}
$$

Here, $d(p_t,w_i)=\lVert p_t-w_i\rVert_2$, $r_w=0.2$ m is the completion radius, and $T_{\max}$ is the episode limit. Intermediate waypoints receive 10 and cause the target index to advance. Final completion receives a base reward of 15 plus a term proportional to the remaining episode steps. Consequently, the terminal reward represents both completion of the entire ordered waypoint set and earlier completion within the episode limit. This time-dependent term is part of the trained objective and must be considered when completion time is interpreted later.

**Safety-Violation Penalty**

Premature termination due to ground collision, overturning, or excessive waypoint deviation receives

$$
r_{\text{penalty}} = - 30
\tag{7}
$$

The angular termination condition is $|\phi|>\pi/2$ or $|\theta|>\pi/2$. The same penalty is applied to each terminating safety event, so the formulation does not assign separate severities to collision, overturning, and excessive waypoint deviation. Instead, it marks all three as outcomes that prematurely end the episode and should be avoided. The numerical threshold for excessive waypoint deviation is not specified in the available manuscript material and is therefore not introduced here.

**Waypoint-Approach Reward**

The waypoint-approach reward $r_{\text{approach}}$ is defined as

$$
r_{approach}=\max\left[0,5.0\left(d(p_{t-1},w_i)-d(p_t,w_i)\right)\right]
\tag{8}
$$

This term is positive only when the distance to waypoint $i$ decreases between consecutive steps. If the distance is unchanged or increases, the maximum operation sets the term to zero rather than adding a separate negative penalty. The reward therefore distinguishes progress from non-progress while the completion and safety terms retain their separate roles.

**Velocity-Alignment Reward**

The velocity-alignment reward is

$$
r_{align}=\max\left(0,0.2\,v_t\cdot\frac{w_i-p_t}{d(p_t,w_i)}\right)
\tag{9}
$$

where $v_t\in\mathbb{R}^3$. The fraction in (9) is the unit vector directed from the current position to waypoint $i$. Its dot product with $v_t$ is positive when the quadcopter velocity contains a component toward the waypoint. Motion perpendicular to the target direction produces a zero dot product, and motion away from the target is removed by the maximum operation. Unlike the approach term, which compares two consecutive distances, the alignment term evaluates the instantaneous relationship between velocity and target direction.

The fixed coefficients in (6)–(9) establish the relative scales of discrete completion, unsafe termination, stepwise progress, and target-directed motion. Because every training run uses the complete reward, the influence of an individual component cannot be claimed without ablation.

## Actor-Critic Network

Proximal Policy Optimization \[11\] uses an Actor–Critic architecture to learn the continuous control policy. The Actor represents the mapping from the current observation to the three velocity-command components, whereas the Critic estimates the value of the observed state to support policy updates. Both networks receive the normalized state $s_t\in\mathbb{R}^{15}$ and contain two fully connected hidden layers with 64 neurons per layer and Tanh activation functions. The Actor output is associated with the three commands in (3), and the Critic produces a scalar state-value estimate.

State normalization reduces scale differences among position error, velocity, attitude, and angular velocity. The available record does not specify its statistics or update rule; these details are therefore not inferred.

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

<img src="assets/figures/figure_03.png" style="width:5.58873in;height:4.33283in" />

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

# RESULTS AND DISCUSSION

1.  **Results**

Proximal Policy Optimization was trained for 500,000 ProjectAirSim interaction steps (Fig. 4). Reward is initially low because the policy has not learned sequential waypoint completion, then increases and fluctuates within a higher range after approximately 350,000 steps. This pattern indicates improved training return under the adopted configuration. Because no quantitative convergence criterion was used, Fig. 4 does not prove mathematical convergence or show that further training could not alter the policy.

<img src="assets/figures/figure_04.png" style="width:4.09482in;height:2.96667in" />

Fig. 4. Training results of the PPO agent.

After training, the policy parameters were frozen. The learned controller and CF were each evaluated ten times on the same helical trajectory, quadcopter, and nominal simulation configuration. These repetitions characterize fixed-controller consistency, not sensitivity to independent training initialization.

<table style="width:99%;">
<colgroup>
<col style="width: 49%" />
<col style="width: 49%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><p><img src="assets/figures/figure_05a.png" style="width:2.85in;height:2.86038in" /></p>
<p>(a) PPO agent</p></th>
<th style="text-align: center;"><p><img src="assets/figures/figure_05b.png" style="width:2.78264in;height:2.79278in" /></p>
<p>(b) CF</p></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: center;">Fig. 5. Three-dimensional flight trajectories.</td>
</tr>
</tbody>
</table>

Both methods completed the waypoints in order (Fig. 5). The learned policy remains close to the reference over most of the helix, with its largest visible deviations where horizontal and vertical motion change simultaneously. CF follows the overall geometry but has larger offsets in several segments, consistent with the aggregate values in Table II. The plots show representative runs; trial-to-trial variation is reported by the table.

<table>
<colgroup>
<col style="width: 49%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th><p><img src="assets/figures/figure_06a.png" style="width:2.96667in;height:0.73353in" /></p>
<p>(a) PPO agent</p></th>
<th><p><img src="assets/figures/figure_06b.png" style="width:3.06698in;height:0.75833in" /></p>
<p>(b) CF</p></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: center;">Fig. 6. Position responses.</td>
</tr>
</tbody>
</table>

Fig. 6 presents position over time and shows faster trajectory progression by the learned policy under the tested settings. CF used $L=0.5$ m and $v_{ref}=1.5m\text{/}s$, whereas the learned policy could use each component up to 3 m/s. Despite common component-wise bounds, the operating speeds were not normalized. The timing difference therefore describes the implemented configurations and is not an intrinsic advantage of the learning algorithm.

<table>
<colgroup>
<col style="width: 49%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th><p><img src="assets/figures/figure_07a.png" style="width:2.96586in;height:0.73333in" /></p>
<p>(a) PPO agent</p></th>
<th><p><img src="assets/figures/figure_07b.png" style="width:3.03326in;height:0.75in" /></p>
<p>(b) CF</p></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: center;">Fig. 7. Attitude responses.</td>
</tr>
</tbody>
</table>

The learned policy produced larger roll and pitch variations during direction changes, whereas CF was smoother; yaw remained small for both methods (Fig. 7). Thus, lower geometric trajectory error did not imply a smoother attitude response. Figs. 5–7 are representative runs, while Table II reports all ten evaluations per method.

Table II. Comparison of PPO and Carrot-Following results.

| Trial | Method | $\mathbf{T}_{\mathbf{sim}\left( \mathbf{s} \right)}$ | RMSE (m) | MAE (m) | $\mathbf{RMS}\mathbf{E}_{\mathbf{x}}\left( \mathbf{m} \right)$ | $\mathbf{RMS}\mathbf{E}_{\mathbf{y}}\left( \mathbf{m} \right)$ | $\mathbf{RMS}\mathbf{E}_{\mathbf{z}}\left( \mathbf{m} \right)$ |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | CF | 24.96 | 0.200 | 0.197 | 0.131 | 0.134 | 0.071 |
|  | PPO | 16.83 | 0.083 | 0.073 | 0.054 | 0.048 | 0.041 |
| 2 | CF | 25.01 | 0.199 | 0.195 | 0.130 | 0.134 | 0.069 |
|  | PPO | 16.93 | 0.082 | 0.072 | 0.053 | 0.047 | 0.041 |
| 3 | CF | 25.03 | 0.198 | 0.195 | 0.130 | 0.134 | 0.067 |
|  | PPO | 16.93 | 0.082 | 0.072 | 0.053 | 0.047 | 0.040 |
| 4 | CF | 24.01 | 0.199 | 0.195 | 0.135 | 0.133 | 0.060 |
|  | PPO | 16.88 | 0.081 | 0.071 | 0.052 | 0.047 | 0.041 |
| 5 | CF | 24.11 | 0.195 | 0.191 | 0.130 | 0.133 | 0.058 |
|  | PPO | 16.93 | 0.081 | 0.072 | 0.052 | 0.047 | 0.041 |
| 6 | CF | 24.09 | 0.195 | 0.191 | 0.131 | 0.132 | 0.058 |
|  | PPO | 16.93 | 0.081 | 0.072 | 0.052 | 0.047 | 0.041 |
| 7 | CF | 25.00 | 0.199 | 0.195 | 0.130 | 0.134 | 0.070 |
|  | PPO | 16.88 | 0.082 | 0.072 | 0.053 | 0.047 | 0.041 |
| 8 | CF | 25.03 | 0.197 | 0.194 | 0.130 | 0.133 | 0.066 |
|  | PPO | 16.93 | 0.081 | 0.072 | 0.053 | 0.047 | 0.040 |
| 9 | CF | 24.11 | 0.194 | 0.191 | 0.130 | 0.132 | 0.058 |
|  | PPO | 16.88 | 0.082 | 0.072 | 0.053 | 0.047 | 0.041 |
| 10 | CF | 24.92 | 0.199 | 0.196 | 0.131 | 0.134 | 0.069 |
|  | PPO | 16.93 | 0.081 | 0.071 | 0.053 | 0.046 | 0.040 |
| Mean | CF | 24.63 | 0.198 | 0.194 | 0.131 | 0.133 | 0.065 |
|  | PPO | 16.91 | 0.082 | 0.072 | 0.053 | 0.047 | 0.041 |
| SD | CF | 0.47 | 0.002 | 0.002 | 0.001 | 0.001 | 0.005 |
|  | PPO | 0.04 | 0.001 | 0.001 | 0.001 | 0.000 | 0.000 |

Mean completion times were 16.91 s for PPO and 24.63 s for CF, corresponding to a 31.3% difference under the implemented controller configurations. This numerical comparison is retained because it describes the observed task durations, but its interpretation is limited by the different speed specifications. CF retained a 1.5-m/s reference magnitude, while the learned controller generated independently bounded velocity components. The result is therefore not a speed-normalized comparison and cannot attribute the entire difference to the controller type.

For geometric trajectory deviation, PPO achieved mean root-mean-square and mean absolute errors of 0.082 and 0.072 m, compared with 0.198 and 0.194 m for CF. These values correspond to reductions of 58.6% and 62.9% under the tested configuration. The same trend appears in the individual axes. PPO's root-mean-square errors in the $x$, $y$, and $z$ directions were 0.053, 0.047, and 0.041 m, respectively, compared with 0.131, 0.133, and 0.065 m for CF. The corresponding reductions were 59.5%, 64.7%, and 36.9%. Because the reference point for each sample is the closest point on the waypoint polyline, these values quantify spatial proximity to the trajectory geometry; they do not measure whether the vehicle and a timed reference reached corresponding locations simultaneously.

Across ten fixed-controller evaluations, the completion-time standard deviation was 0.04 s for PPO and 0.47 s for CF. Root-mean-square and mean absolute error standard deviations were 0.001 m for PPO and 0.002 m for CF. These values describe nominal repeated execution, not independently trained policies. Values displayed as 0.000 after rounding do not imply exactly zero variation.

2.  **Discussion**

The lower geometric errors obtained by PPO may be associated with the information included in its state representation. The current-waypoint error identifies the immediate target, while the next-waypoint error provides information about the upcoming segment. This combination can make a change in local trajectory direction observable before the current target is completed. Nevertheless, the complete state was used throughout training and evaluation. Without an otherwise identical experiment that removes the next-waypoint components, the specific contribution of those inputs cannot be separated from the effects of the remaining state variables, the reward, and the learned policy.

The approach and alignment rewards provide feedback between discrete waypoint completions. The first is positive when the target distance decreases from one step to the next, and the second is positive when the current velocity has a component toward the waypoint. Together, they make task-related feedback available more frequently than a completion-only formulation. The experiment, however, evaluates only the complete four-term reward. No training runs remove or rescale individual terms, so their separate contributions and the sensitivity to the fixed coefficients remain unquantified.

Lower PPO trajectory deviation coincided with larger visible roll and pitch variations, suggesting a possible trade-off between spatial tracking and motion smoothness. The learned controller generated three independently bounded velocity components, whereas CF directed a fixed-magnitude velocity vector toward a look-ahead point. The controllers also progressed at different rates, which can affect the attitude changes needed to redirect the vehicle. These distinctions offer plausible context for the plotted responses but do not establish a causal explanation. No command-variation, attitude-rate, or smoothness metric was computed, so the comparison remains observational.

The training objective itself also affects the interpretation of task duration. The 400-step episode limit bounds the available time, and the final-waypoint reward increases with the number of remaining steps. The learned policy is therefore explicitly encouraged to complete the sequence early. Combined with CF's fixed 1.5-m/s reference speed and the learned policy's independently bounded components, these design choices prevent attribution of the completion-time difference to Proximal Policy Optimization alone. A controlled timing comparison would require equivalent speed constraints and a protocol that separates the effect of the learned objective from the effect of the guidance strategy.

Evaluation was limited to ProjectAirSim, one helical trajectory, one fixed set of learned weights, and a nominal configuration without explicitly introduced wind, sensor noise, delay, or model uncertainty. The repeated trials do not cover alternative trajectory shapes, payloads, vehicle parameters, disturbance levels, or training seeds. In addition, the trajectory-deviation metric is geometric rather than time-parameterized, and no physical-quadcopter experiment was conducted. Accordingly, the results support the feasibility of high-level learned velocity guidance for waypoint trajectory tracking in this specific scenario. They do not establish general superiority over conventional methods, robustness to unmodelled conditions, or effectiveness on a real vehicle.

# CONCLUSION

This study developed and evaluated a Proximal Policy Optimization controller for waypoint trajectory tracking control of a quadcopter in ProjectAirSim. The controller used a fifteen-dimensional state combining vehicle motion and attitude with relative errors to the current and next waypoints. It generated velocity commands along the three North–East–Down axes, while the simulator's built-in flight controller executed the low-level stabilization. The reward represented waypoint completion, unsafe termination, progress toward the current target, and velocity alignment.

After 500,000 interaction steps, the learned weights were fixed. The resulting controller and Carrot-Following were each evaluated ten times on the same forty-waypoint helical trajectory, quadcopter configuration, and nominal simulation environment. Both controllers completed the prescribed waypoint sequence. These repeated trials characterize the behavior of the fixed controller configurations in the selected trajectory tracking scenario rather than variation across independently trained policies.

Proximal Policy Optimization achieved a mean completion time, geometric trajectory-deviation root-mean-square error, and mean absolute error of 16.91 s, 0.082 m, and 0.072 m, respectively, compared with 24.63 s, 0.198 m, and 0.194 m for Carrot-Following. The learned controller therefore maintained smaller geometric deviations from the waypoint trajectory under the tested configurations. However, the completion-time comparison was not speed-normalized because Carrot-Following used a fixed reference-speed magnitude of 1.5 m/s, whereas the learned controller could issue larger commands within the common component-wise bounds. Moreover, the error metrics measure distance to the waypoint polyline rather than synchronization with a time-parameterized reference trajectory.

The learned controller produced larger roll and pitch variations during direction changes. Its lower geometric trajectory deviation therefore did not correspond to the smoothest visible attitude response. The low standard deviations in the reported metrics describe repeated evaluations of the fixed controllers and should not be interpreted as evidence of low sensitivity to the policy-training process.

Overall, the results support the feasibility of Proximal Policy Optimization for high-level waypoint trajectory tracking control in the investigated ProjectAirSim scenario. This conclusion is limited to one helical trajectory, nominal simulation conditions, unmatched operating speeds, and one fixed set of learned weights. The absence of hardware experiments, reward and state ablations, disturbance tests, and multi-seed training evaluation prevents broader claims of robustness, real-world effectiveness, or general superiority. Further work should evaluate additional waypoint trajectories and disturbances, use equivalent speed constraints, quantify command and attitude smoothness, repeat training with multiple seeds, and validate the controller on a physical quadcopter.

# REFERENCES

1.  M. F. Ahmed, J. C. Mohanta, and M. N. Zafar, “Development of smart quadcopter for autonomous overhead power transmission line inspections,” Mater. Today Proc., vol. 51, pp. 261–268, 2022, doi: 10.1016/j.matpr.2021.05.271.

2.  I. Martinez-Alpiste, G. Golcarenarenji, Q. Wang, and J. M. Alcaraz Calero, “Search and rescue operation using UAVs: A case study,” Expert Syst. Appl., vol. 178, Art. no. 114937, Sep. 2021, doi: 10.1016/j.eswa.2021.114937.

3.  M. A. Abitha and A. Saleem, “Quadrotor Modeling Approaches and Trajectory Tracking Control Algorithms: A Review,” International Journal of Robotics and Control Systems, vol. 4, no. 1, pp. 401–426, Apr. 2024, doi: 10.31763/ijrcs.v4i1.1324.

4.  M. Rabah, A. Rohan, Y.-J. Han, and S.-H. Kim, “Design of Fuzzy-PID Controller for Quadcopter Trajectory-Tracking,” International Journal of Fuzzy Logic and Intelligent Systems, vol. 18, no. 3, pp. 204–213, Sep. 2018, doi: 10.5391/IJFIS.2018.18.3.204.

5.  D. Rodriguez-Guevara, A. Favela-Contreras, and O. J. Gonzalez Villarreal, “A qLPV-MPC Control Strategy for Trajectory Tracking of Quadrotors,” Machines, vol. 11, no. 7, Art. no. 755, Jul. 2023, doi: 10.3390/machines11070755.

6.  D. J. Almakhles, “Robust Backstepping Sliding Mode Control for a Quadrotor Trajectory Tracking Application,” IEEE Access, vol. 8, pp. 5515–5525, 2020, doi: 10.1109/ACCESS.2019.2962722.

7.  P. Caffyn Yuste, J. A. Iglesias Martínez, and M. A. Sanchis De Miguel, “Simulation-based evaluation of model-free reinforcement learning algorithms for quadcopter attitude control and trajectory tracking,” Neurocomputing, vol. 608, Art. no. 128362, Dec. 2024, doi: 10.1016/j.neucom.2024.128362.

8.  T. Y. Trad et al., “Real-Time Implementation of Quadrotor UAV Control System Based on a Deep Reinforcement Learning Approach,” Comput. Mater. Continua, vol. 81, no. 3, pp. 4757–4786, 2024, doi: 10.32604/cmc.2024.055634.

9.  J. Wu, Z. Yang, L. Liao, N. He, Z. Wang, and C. Wang, “A State Compensated Deep Deterministic Policy Gradient Algorithm for UAV Trajectory Tracking,” Machines, vol. 10, no. 7, Art. no. 496, Jun. 2022, doi: 10.3390/machines10070496.

10. Y. Mahran, Z. Gamal, and A. El-Badawy, “Reinforcement Learning Position Control of a Quadrotor Using Soft Actor-Critic (SAC),” in Proc. 6th Novel Intell. Leading Emerging Sci. Conf. (NILES), Oct. 2024, pp. 72–75, doi: 10.1109/NILES63360.2024.10753187.

11. J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal Policy Optimization Algorithms,” arXiv:1707.06347, Jul. 2017.

12. IAMAI Consulting Corp., “Project AirSim,” GitHub repository. [Online]. Available: https://github.com/iamaisim/ProjectAirSim. [Accessed: Nov. 10, 2026].

13. M. Towers et al., “Gymnasium: A Standard Interface for Reinforcement Learning Environments,” arXiv:2407.17032, Jul. 2024, doi: 10.48550/arXiv.2407.17032.

14. H. Pérez-León, J. J. Acevedo, J. A. Millán-Romera, A. Castillejo-Calle, I. Maza, and A. Ollero, “An Aerial Robot Path Follower Based on the ‘Carrot Chasing’ Algorithm,” in Robot 2019: Fourth Iberian Robotics Conference, Advances in Intelligent Systems and Computing, vol. 1093, Springer, 2020, pp. 37–47, doi: 10.1007/978-3-030-36150-1_4.

15. J. Schulman, P. Moritz, S. Levine, M. I. Jordan, and P. Abbeel, “High-Dimensional Continuous Control Using Generalized Advantage Estimation,” in Proc. Int. Conf. Learn. Represent. (ICLR), 2016.
