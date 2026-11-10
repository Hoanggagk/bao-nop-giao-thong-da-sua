# RESULTS AND DISCUSSION

1.  **Result**

The results cover PPO training, post-training trajectory and attitude responses, and completion time and tracking errors over ten trials against CF. The PPO agent is trained for 500,000 interaction steps in ProjectAirSim (Fig. 4). Reward is initially low because the agent has not learned to approach and complete waypoints sequentially. It increases with training and, from approximately 350,000 steps, fluctuates within a higher-value region with smaller variations. This indicates progressive improvement in task-appropriate velocity commands. Without a separate quantitative convergence criterion, however, Fig. 4 does not establish mathematical convergence.

<img src="../assets/figures/figure_04.png" style="width:4.09482in;height:2.96667in" />

Fig. 4. Training results of the PPO agent.

After training, the PPO-agent weights are fixed and the agent is evaluated on a helical trajectory consisting of 40 waypoints with radius r = 1.5 m. In the NED frame, the z coordinate of the trajectory varies from −2.0 m at the initial point to −4.0 m at the final point. CF is used as the reference method. Both methods are evaluated on the same helical trajectory, with the same quadcopter configuration and simulation environment; each method is executed ten times under the same test scenario.

<table style="width:99%;">
<colgroup>
<col style="width: 49%" />
<col style="width: 49%" />
</colgroup>
<thead>
<tr>
<th style="text-align: center;"><p><img src="../assets/figures/figure_05a.png" style="width:2.85in;height:2.86038in" /></p>
<p>(a) PPO agent</p></th>
<th style="text-align: center;"><p><img src="../assets/figures/figure_05b.png" style="width:2.78264in;height:2.79278in" /></p>
<p>(b) CF</p></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: center;">Fig. 5. Three-dimensional flight trajectories.</td>
</tr>
</tbody>
</table>

Fig. 5 shows that both methods complete the helical trajectory in the prescribed waypoint order. PPO remains relatively close to the reference path, with the largest deviations mainly where horizontal and vertical motion change simultaneously. CF exhibits larger deviations in several segments, consistent with Table II.

<table>
<colgroup>
<col style="width: 49%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th><p><img src="../assets/figures/figure_06a.png" style="width:2.96667in;height:0.73353in" /></p>
<p>(a) PPO agent</p></th>
<th><p><img src="../assets/figures/figure_06b.png" style="width:3.06698in;height:0.75833in" /></p>
<p>(b) CF</p></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: center;">Fig. 6. Position responses.</td>
</tr>
</tbody>
</table>

Whereas Fig. 5 shows the three-dimensional trajectory shape, Fig. 6 presents the time histories of position to clarify the rate of progression along the trajectory. PPO completes the trajectory in less time than CF under the specified controller parameters. However, because CF uses $v_{ref} = 1.5m\text{/}s$ while PPO can generate each velocity component up to 3 m/s, the difference in completion time should not be attributed solely to an intrinsic advantage of the PPO policy. The timing results should be interpreted together with the tracking errors and the velocity constraints of the two methods.

<table>
<colgroup>
<col style="width: 49%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th><p><img src="../assets/figures/figure_07a.png" style="width:2.96586in;height:0.73333in" /></p>
<p>(a) PPO agent</p></th>
<th><p><img src="../assets/figures/figure_07b.png" style="width:3.03326in;height:0.75in" /></p>
<p>(b) CF</p></th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="2" style="text-align: center;">Fig. 7. Attitude responses</td>
</tr>
</tbody>
</table>

Fig. 7 shows larger PPO roll and pitch variations, particularly during direction changes, whereas CF produces smoother attitude responses with smaller amplitudes. Yaw remains relatively small for both methods. Thus, faster PPO motion is accompanied by greater attitude variation. Figs. 5–7 present representative runs; Table II reports individual results, means, and standard deviations from ten evaluations per method under the same scenario.

Table 2. Comparison of ppo and carrot-following results

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

In terms of completion time, PPO achieves a mean value of 16.91 s, compared with 24.63 s for CF, corresponding to a difference of approximately 31.3% under the controller configurations used. Because the two methods do not employ the same speed-magnitude limit, this result reflects only the completion times of the implemented configurations and should not be interpreted as a speed-normalized comparison. In terms of trajectory-tracking accuracy, PPO achieves a mean RMSE of 0.082 m and a mean MAE of 0.072 m, lower than the corresponding CF values of 0.198 m and 0.194 m; the respective reductions are approximately 58.6% and 62.9%. A similar trend is observed on each axis: the PPO RMSE_x, RMSE_y, and RMSE_z values are 0.053, 0.047, and 0.041 m, respectively, compared with 0.131, 0.133, and 0.065 m for CF. The corresponding reductions are approximately 59.5%, 64.7%, and 36.9%. Under the investigated conditions, PPO therefore maintains lower tracking errors than CF along all three axes.

In addition to the mean values, the standard deviations over ten trials indicate low variability in the PPO metrics. The standard deviation of completion time is 0.04 s for PPO, compared with 0.47 s for CF; the standard deviations of the PPO RMSE and MAE are both 0.001 m, whereas those of CF are 0.002 m. The standard-deviation values are rounded to the number of digits displayed in the table; consequently, values shown as 0.000 should not be interpreted as indicating absolutely zero variability across runs.

1.  **Dicussion**

PPO’s lower tracking errors may be associated with its state representation: the current-waypoint error defines the immediate target, while the next-waypoint error indicates the upcoming path direction. This information may help reduce deviations during waypoint transitions. On the helical trajectory, mean RMSE and MAE were 0.082 and 0.072 m for PPO, versus 0.198 and 0.194 m for CF. Without an ablation excluding next-waypoint information, however, its individual contribution cannot be quantified.

The reward design may also support tracking. Alongside completion and safety terms, the waypoint-approach reward encourages decreasing target distance and the velocity-alignment reward promotes target-directed motion. These continuous terms provide feedback before waypoint completion and reduce reward sparsity. The experiments assess the complete formulation; the contribution of each term requires an ablation study.

The lower PPO tracking errors are accompanied by larger roll and pitch variations during direction changes (Fig. 7), suggesting a trade-off between tracking performance and motion smoothness. PPO generates three independently bounded velocity components, whereas CF directs a fixed-magnitude velocity vector toward the carrot point. These differences may partly explain the attitude responses, but no dedicated command-smoothness or attitude-variation metrics were computed. The interpretation therefore remains observational; future evaluation should quantify command variation or attitude rates.

Velocity constraints also differ: CF uses a fixed speed magnitude of 1.5 m/s, while each PPO command component lies within \[−3, 3\] m/s. The mean completion times of 16.91 s and 24.63 s therefore describe the implemented configurations and do not establish an intrinsic PPO speed advantage. Equivalent velocity constraints are needed to isolate the control strategy’s effect on completion time.

Evaluation is limited to ProjectAirSim, one helical trajectory, and no explicitly introduced wind or model uncertainty. The repeated trials assess the fixed post-training controller in one scenario, not variability across PPO training seeds. The results support the framework’s feasibility rather than general superiority over conventional methods. Further evaluation should include different trajectory geometries, disturbances, model uncertainties, equivalent velocity constraints, and physical-quadcopter tests.
