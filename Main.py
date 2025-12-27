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


# Define Forces
pm = ForceModels.PointMassGravity(Earth)
tb = ForceModels.nBodyGravity(Moon)
j2 = ForceModels.J2Gravity(Earth)

# Concatenate Forces
Dynamics = IntegratorModels.Dynamics([pm, tb, j2])

# Run RK4
integrator_RK4 = IntegratorModels.RK4Integrator()
SpaceVehicle_RK4.StateProperties.stateHistory = PropagatorModels.Propagate(SpaceVehicle_RK4.StateProperties.state, 
                                                                           TimeElement, 
                                                                           integrator_RK4, 
                                                                           Dynamics)

# Run Unit Test
UnitTestSpaceVehicle = UnitTestModule.TwoBodyPropagationTest()

# Create a Color Scheme
Scheme = ColorSchemeObjects.VisualScheme_RetroMilitary()
Fig = StandardPlots.FigureObject(Scheme)
StandardPlots.Plot_Body(Earth)
StandardPlots.Plot_Body(Moon)

StandardPlots.Plot_Trajectory(SpaceVehicle_RK4)
StandardPlots.Plot_Trajectory(UnitTestSpaceVehicle)


# Error Plot
Error_RK4 = SpaceVehicle_RK4.StateProperties.stateHistory - UnitTestSpaceVehicle.StateProperties.stateHistory

fig, axes = plt.subplots(2, 3, sharey='row')

t_err = np.arange(len(Error_RK4))
t_state = np.arange(len(SpaceVehicle_RK4.StateProperties.stateHistory))

# ----- Row 0: Errors -----
axes[0, 0].plot(t_err, Error_RK4[:, 0], color='#4aff00')
axes[0, 0].set_title("X Offset")
axes[0, 0].grid(True)
axes[0, 0].ticklabel_format(style='plain', axis='y', useOffset=False)

axes[0, 1].plot(t_err, Error_RK4[:, 1], color='#4aff00')
axes[0, 1].set_title("Y Offset")
axes[0, 1].grid(True)
axes[0, 1].ticklabel_format(style='plain', axis='y', useOffset=False)

axes[0, 2].plot(t_err, Error_RK4[:, 2], color='#4aff00')
axes[0, 2].set_title("Z Offset")
axes[0, 2].grid(True)
axes[0, 2].ticklabel_format(style='plain', axis='y', useOffset=False)

# ----- Row 1: States -----
axes[1, 0].plot(t_state, SpaceVehicle_RK4.StateProperties.stateHistory[:, 0],color='#4aff00')
axes[1, 0].plot(t_state,UnitTestSpaceVehicle.StateProperties.stateHistory[:, 0],color='#CC1100')
axes[1, 0].set_title("X")
axes[1, 0].grid(True)
axes[1, 0].ticklabel_format(style='plain', axis='y', useOffset=False)

axes[1, 1].plot(t_state,SpaceVehicle_RK4.StateProperties.stateHistory[:, 1],color='#4aff00')
axes[1, 1].plot(t_state,UnitTestSpaceVehicle.StateProperties.stateHistory[:, 1],color='#CC1100')
axes[1, 1].set_title("Y")
axes[1, 1].set_title("Y")
axes[1, 1].grid(True)
axes[1, 1].ticklabel_format(style='plain', axis='y', useOffset=False)


axes[1, 2].plot(t_state,SpaceVehicle_RK4.StateProperties.stateHistory[:, 2],color='#4aff00')
axes[1, 2].plot(t_state,UnitTestSpaceVehicle.StateProperties.stateHistory[:, 2],color='#CC1100')
axes[1, 2].set_title("Z")
axes[1, 2].grid(True)
axes[1, 2].ticklabel_format(style='plain', axis='y', useOffset=False)


plt.tight_layout()
plt.show()
