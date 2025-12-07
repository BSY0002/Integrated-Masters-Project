import numpy as np
import CommonObjects as CommonObjects
import matplotlib.pyplot as plt
import PlottingObjects as Plotting_Objects
import ColorSchemeObjects as Color_Scheme
import PropagatorObjects as Propagator_Objects


# Example
System = CommonObjects.SystemObject("Earth-Satellite System")

# Define the Earth
Earth = CommonObjects.Planet("Earth")
Earth.state_properties.position = np.array([0.0, 0.0, 0.0])
Earth.state_properties.velocity = np.array([0.0, 0.0, 0.0])
Earth.physical_properties.mass = 5.972e24  # kg
Earth.physical_properties.radius = 6371.0  # km
Earth.visual_properties.setColorScheme(Color_Scheme.ColorScheme.VisualScheme_RetroMilitary.Primary)

# Define the Moon
Moon = CommonObjects.Planet("Moon")
Moon.state_properties.position = np.array([384400.0, 0.0, 0.0])  # km
Moon.state_properties.velocity = np.array([0.0, 1.022, 0.0])  # km/s
Moon.physical_properties.mass = 7.342e22  # kg
Moon.physical_properties.radius = 1737.1  # km
Moon.visual_properties.setColorScheme(Color_Scheme.ColorScheme.VisualScheme_RetroMilitary.Secondary)

# Define the Test Satellite
Satellite1 = CommonObjects.SpaceVehicle("Satellite")
Satellite1.state_properties.position = np.array([7000.0, 0.0, 0.0])
Satellite1.state_properties.velocity = np.array([0.0, 7.5, 0.0]) 
Satellite1.visual_properties.setColorScheme(Color_Scheme.ColorScheme.VisualScheme_RetroMilitary.Tertiary)

# Define the Propagator
TwoBodyPropagator = Propagator_Objects.TwoBodyPropagator()
TwoBodyPropagator.body_list = [Earth, Satellite1]
TwoBodyPropagator.time_vector = np.array([0, 3600])  # 1 hour propagation
TwoBodyPropagator.Propagate()

# Plotting
Figure1 = Plotting_Objects.FigureObject()
Figure1.setColorScheme(Color_Scheme.ColorScheme.VisualScheme_RetroMilitary.Figure)
Plotting_Objects.Plot_Body(Earth)
Plotting_Objects.Plot_Trajectory(Satellite1)


# Define the second Test Satellite
Satellite2 = CommonObjects.SpaceVehicle("Satellite2")
Satellite2.state_properties.position = np.array([46128.00000000, 0.00000000, 0.00000000])
Satellite2.state_properties.velocity = np.array([0.00000000, 3.56542303, 0.00000000]) 

Satellite2.visual_properties.setColorScheme(Color_Scheme.ColorScheme.VisualScheme_RetroMilitary.Tertiary)

# Define CR3BP Propagator
ThreeBodyPropagator = Propagator_Objects.CircularRestrictedThreeBodyPropagator()
ThreeBodyPropagator.body_list = [Earth, Moon, Satellite2]
ThreeBodyPropagator.time_vector = np.linspace(0, 500*86400, 1000)  # 1 day propagation
ThreeBodyPropagator.Propagate()

Figure2 = Plotting_Objects.FigureObject()
Figure2.setColorScheme(Color_Scheme.ColorScheme.VisualScheme_RetroMilitary.Figure)
Plotting_Objects.Plot_Trajectory(Satellite2)
Plotting_Objects.Plot_Body(Earth)
Plotting_Objects.Plot_Body(Moon)



plt.show()
