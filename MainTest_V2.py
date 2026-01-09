import ForceModels 
import IntegratorModels
import TimeModule 
import ObjectModels
import numpy as np
import PropagatorModels
import ColorSchemeObjects
import StandardPlots
import matplotlib.pyplot as plt
import time
from matplotlib.patches import Circle
from matplotlib.ticker import ScalarFormatter

# Begin Script
start_time = time.time()  # record start
print('----------------')
print('Code Start')
print('----------------')

## Create Time Elemenet
TimeElement = TimeModule.Time()
TimeElement.endTime = 2551443/10000

## Create Objects
Earth = ObjectModels.Earth()
LEOSatellite = ObjectModels.LEOSpaceVehicle()

## Create Integrators
integrator_RK45Adaptive = IntegratorModels.AdaptiveRK45Integrator()

#=========================
## Earth Properties
#=========================
Earth.IntegratorProperties.orbit.dynamics = IntegratorModels.OrbitDynamics([ForceModels.Fixed])
Earth.IntegratorProperties.orbit.integrator = integrator_RK45Adaptive
Earth.IntegratorProperties.attitude.integrator = integrator_RK45Adaptive
Earth.IntegratorProperties.attitude.dynamics = IntegratorModels.AttitudeDynamics(torques = [ForceModels.NullTorque()], body = Earth )

#=========================
## LEO Sat Properties
#=========================
LEOSatellite.IntegratorProperties.orbit.dynamics = IntegratorModels.OrbitDynamics([ForceModels.PointMassGravity(Earth)])
LEOSatellite.IntegratorProperties.orbit.integrator = integrator_RK45Adaptive
LEOSatellite.IntegratorProperties.attitude.integrator = integrator_RK45Adaptive
LEOSatellite.IntegratorProperties.attitude.dynamics = IntegratorModels.AttitudeDynamics(torques = [ForceModels.NullTorque()], body = LEOSatellite )
LEOSatellite.IntegratorProperties.attitude.dt_max = 10
#=========================
## Propagator
#=========================
bodyList = [Earth, LEOSatellite]
PropagatorModels.Propagate(bodyList, TimeElement)

#=========================
## Plotting
#=========================
Scheme = ColorSchemeObjects.VisualScheme_RetroMilitary()
Fig = StandardPlots.FigureObject(Scheme)

AtmosCircle = Circle((0,0), Earth.PhysicalProperties.radius + 2000e3, edgecolor='red', facecolor='red', alpha = .1, linewidth=1)
EarthSurfaceCircle = Circle((0,0), Earth.PhysicalProperties.radius, edgecolor='blue', facecolor='blue', alpha = 1, linewidth=2)
Fig.ax.add_patch(AtmosCircle)
Fig.ax.add_patch(EarthSurfaceCircle)

for body in bodyList:
    StandardPlots.Plot_Body(body)
    StandardPlots.Plot_Trajectory(body)

Ani = StandardPlots.Animate_Trajectories(bodyList, Fig)

end_time = time.time()
duration = end_time - start_time
print(f"Script runtime: {duration:.4f} seconds")

## Code End
print('----------------')
print('Code End')
print('----------------')





############
#Extra Plots
############
S = LEOSatellite
z_axis = S.StateProperties.attitude_stateHistory  # shape: (N, 7)
times = S.StateProperties.attitude_times          # shape: (N,)

if z_axis is not None and times is not None:

    # Quaternion norms
    quat_norms = np.linalg.norm(z_axis[:, 0:4], axis=1)

    # Angular velocity
    w = z_axis[:, 4:7]  # [wx, wy, wz]

    # Angular acceleration (numerical derivative)
    dt = np.diff(times)
    alpha = np.diff(w, axis=0) / dt[:, None]  # shape: (N-1, 3)

    # For plotting, align alpha with midpoint times
    t_alpha = (times[:-1] + times[1:]) / 2

    # Set up figure
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))

    # -----------------------------
    # 1) Quaternions
    # -----------------------------
    ax[0].plot(times, z_axis[:,0], label='q0')
    ax[0].plot(times, z_axis[:,1], label='q1')
    ax[0].plot(times, z_axis[:,2], label='q2')
    ax[0].plot(times, z_axis[:,3], label='q3')
    ax[0].set_title("Quaternions")
    ax[0].set_xlabel("Time [s]")
    ax[0].legend()
    ax[0].grid(True)

    # -----------------------------
    # 2) Quaternion norm
    # -----------------------------
    ax[1].plot(times, quat_norms, label='||q||')
    ax[1].set_title("Quaternion Norm")
    ax[1].set_xlabel("Time [s]")
    ax[1].legend()
    ax[1].grid(True)

    ax[1].yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    ax[1].ticklabel_format(style='plain', axis='y')

    # -----------------------------
    # 3) Angular velocity and acceleration
    # -----------------------------
    ax[2].plot(times, w[:,0], label='wx')
    ax[2].plot(times, w[:,1], label='wy')
    ax[2].plot(times, w[:,2], label='wz')
    ax[2].set_title("Angular velocity")
    ax[2].set_xlabel("Time [s]")
    ax[2].legend()
    ax[2].grid(True)

    plt.tight_layout()
    plt.show()