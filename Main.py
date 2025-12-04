import numpy as np
import CommonObjects as CommonObjects
import matplotlib.pyplot as plt
import PlottingObjects as Plotting_Objects
import ColorSchemeObjects as Color_Scheme



# Example
System = CommonObjects.SystemObject("Earth-Satellite System")
Satellite = CommonObjects.SpaceVehicle("Satellite")
Earth = CommonObjects.Planet("Earth")

Earth.state_properties.position = np.array([0.0, 0.0, 0.0])

Satellite.state_properties.position = np.array([7000.0, 0.0, 0.0])
Satellite.state_properties.velocity = np.array([0.0, 7.5, 0.0]) 
Satellite.state_properties.stateHistory = np.array([
                                                [7000.0, 0.0, 0.0],
                                                [7000.0, 100.0, 0.0],
                                                [6990.0, 75.0, 0.0],
                                                [6960.0, 150.0, 0.0],
                                                [6920.0, 225.0, 0.0]])


Figure1 = Plotting_Objects.FigureObject()
Figure1.setColorScheme(Color_Scheme.ColorScheme.VisualScheme_Default.Figure)
Satellite.visual_properties.setColorScheme(Color_Scheme.ColorScheme.VisualScheme_Default.Tertiary)
Earth.visual_properties.setColorScheme(Color_Scheme.ColorScheme.VisualScheme_Default.Primary)
Plotting_Objects.Plot_Body(Earth)
Plotting_Objects.Plot_Body(Satellite)
Plotting_Objects.Plot_Trajectory(Satellite)

Figure1 = Plotting_Objects.FigureObject()
Figure1.setColorScheme(Color_Scheme.ColorScheme.VisualScheme_RetroMilitary.Figure)
Satellite.visual_properties.setColorScheme(Color_Scheme.ColorScheme.VisualScheme_RetroMilitary.Tertiary)
Earth.visual_properties.setColorScheme(Color_Scheme.ColorScheme.VisualScheme_RetroMilitary.Primary)
Plotting_Objects.Plot_Body(Earth)
Plotting_Objects.Plot_Body(Satellite)
Plotting_Objects.Plot_Trajectory(Satellite)


plt.show()
