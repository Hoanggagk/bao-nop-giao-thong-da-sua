# 2. WAYPOINT TRAJECTORY TRACKING PROBLEM

The control objective is to guide the quadcopter sequentially through the waypoint set $W = \{w_{1},\ldots,w_{N}\}$ in three-dimensional space, as illustrated in Fig. 1. The $i$th waypoint is $w_{i} = [x_{i},y_{i},z_{i}]^{T}$, and the position at control instant $t$ is $p_{t} = [x_{t},y_{t},z_{t}]^{T}$. Both are expressed in the inertial North–East–Down frame. The task is not merely to reach the final location, but to complete the intermediate targets in their prescribed order.

<img src="../assets/figures/figure_01.png" style="width:6.11501in;height:2.33333in" />

Fig. 1. Waypoint trajectory tracking control problem for the quadcopter.

Two coordinate frames describe the motion. The inertial frame $\{I\}$ defines global position, where $X_I$, $Y_I$, and $Z_I$ correspond to North, East, and Down. The body-fixed frame $\{B\}$ is attached to the quadcopter and contains $x_B$, $y_B$, and $z_B$. Vehicle attitude relates the moving frame to the inertial frame, while the waypoints and translational-velocity commands use North–East–Down coordinates.

At each control instant, one waypoint $w_i$ is designated as the current target. The relative position between the quadcopter and this target provides the immediate direction and distance information used by the policy. When the waypoint-completion condition is satisfied, the target index advances from $i$ to $i+1$. This switching process continues until the final waypoint $w_N$ has been reached. The next waypoint is also included in the policy state so that the observation contains information about the local continuation of the trajectory rather than only the current point target.

Under this formulation, a successful controller must satisfy several objectives simultaneously. It must complete the waypoint sequence without triggering the stated termination conditions, remain close to the piecewise-linear path defined by the waypoints, and complete the task within the episode duration. These objectives are related but not identical: a controller can reach every waypoint while deviating between them, and a shorter completion time can be produced by a higher operating speed rather than by a better guidance law. For this reason, the experimental evaluation reports completion time together with geometric trajectory-deviation measures and interprets timing in light of the velocity settings used by each method.
