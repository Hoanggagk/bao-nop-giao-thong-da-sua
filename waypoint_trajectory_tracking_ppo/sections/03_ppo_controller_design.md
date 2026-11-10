# PPO-BASED CONTROLLER DESIGN

Fig. 2 shows the hierarchical architecture used in this study. Proximal Policy Optimization maps vehicle-state and waypoint information to velocity commands in the North–East–Down frame, and ProjectAirSim's low-level flight controller executes these commands \[12\]. The learned policy therefore determines the desired translational motion but does not replace the inner stabilization loops. Position, linear velocity, Euler angles, and angular velocity are returned at the next control instant to close the feedback loop. This division of responsibility makes the policy output directly comparable with the velocity command used by the reference method while retaining the simulator's established mechanism for converting desired motion into vehicle-level actuation.

<img src="../assets/figures/figure_02.png" style="width:4.90639in;height:2.45833in" />

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
