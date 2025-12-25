import ForceModels 
import IntegratorModels
import TimeModule 
import numpy as np
import matplotlib.pyplot as plt
import UnitTestModule
import PropagatorModels
import ObjectModels
import ColorSchemeObjects
import StandardPlots

# Create Simulation Settings
TimeElement = TimeModule.Time()

# Create Planetary Objects
Earth = ObjectModels.Earth()
Moon = ObjectModels.Moon()



# Create Test Space Vehicles
SpaceVehicle_RK4 = ObjectModels.TestSpaceVehicle()
SpaceVehicle_RK4.name = "RK4 Test Vehicle"

SpaceVehicle_DOPI5 = ObjectModels.TestSpaceVehicle()
SpaceVehicle_DOPI5.name = "DOPI5 Test Vehicle"

# Define Forces
pm = ForceModels.PointMassGravity(Earth.PhysicalProperties.mu)
j2 = ForceModels.J2Gravity(Earth.PhysicalProperties.mu, 
                           Earth.PhysicalProperties.radius, 
                           Earth.PhysicalProperties.J2)

# Concatenate Forces
Dynamics = IntegratorModels.Dynamics([pm])

# Run DOPI5
integrator_DOPI5 = IntegratorModels.DOPRI5Integrator()
SpaceVehicle_DOPI5.StateProperties.stateHistory = PropagatorModels.Propagate(SpaceVehicle_DOPI5.StateProperties.state, TimeElement, integrator_DOPI5, Dynamics)

# Run RK4
integrator_RK4 = IntegratorModels.RK4Integrator()
SpaceVehicle_RK4.StateProperties.stateHistory = PropagatorModels.Propagate(SpaceVehicle_RK4.StateProperties.state, TimeElement, integrator_RK4, Dynamics)

# Run Unit Test
state_UnitTest_history = UnitTestModule.TwoBodyPropagationTest()

# Test Plots

# Create a Color Scheme
Scheme = ColorSchemeObjects.VisualScheme_Default()
Fig = StandardPlots.FigureObject(Scheme)
StandardPlots.Plot_Body(Earth)
StandardPlots.Plot_Trajectory(SpaceVehicle_RK4)
StandardPlots.Plot_Trajectory(SpaceVehicle_DOPI5)



fig, ax = plt.subplots()
RK4 = ax.scatter(           SpaceVehicle_RK4.StateProperties.stateHistory[:, 0], 
                            SpaceVehicle_RK4.StateProperties.stateHistory[:, 1],
                            linewidth   = 1,
                            alpha       = 1,
                            zorder      = 99,
                            color       = 'blue',
                            s        = .1
)
DOR = ax.scatter(           SpaceVehicle_DOPI5.StateProperties.stateHistory[:, 0], 
                            SpaceVehicle_DOPI5.StateProperties.stateHistory[:, 1],
                            linewidth   = 1,
                            alpha       = 1,
                            zorder      = 99,
                            color       = 'red',
                            s        = .1
)

UnitTest = ax.scatter(      state_UnitTest_history[:, 0], 
                            state_UnitTest_history[:, 1],
                            linewidth   = 1,
                            alpha       = 1,
                            zorder      = 99,
                            color       = 'green',
                            s        = .1
)
plt.grid(True)

# Error Plot
Error_RK4 = SpaceVehicle_RK4.StateProperties.stateHistory - state_UnitTest_history
Error_DOPI5 = SpaceVehicle_DOPI5.StateProperties.stateHistory - state_UnitTest_history

fig, axes = plt.subplots(1, 3, sharey=True)

axes[0].plot(np.arange(len(Error_RK4)), Error_RK4[:, 0], color = 'blue')
axes[0].plot(np.arange(len(Error_DOPI5)), Error_DOPI5[:, 0], color = 'red')
axes[0].set_title("X Error")
axes[0].grid(True)

axes[1].plot(np.arange(len(Error_RK4)), Error_RK4[:, 1], color = 'blue')
axes[1].plot(np.arange(len(Error_DOPI5)), Error_DOPI5[:, 1], color = 'red')
axes[1].set_title("Y Error")
axes[1].grid(True)

axes[2].plot(np.arange(len(Error_RK4)), Error_RK4[:, 2], color = 'blue')
axes[2].plot(np.arange(len(Error_DOPI5)), Error_DOPI5[:, 2], color = 'red')
axes[2].set_title("Z Error")
axes[2].grid(True)

plt.tight_layout()
plt.show()
