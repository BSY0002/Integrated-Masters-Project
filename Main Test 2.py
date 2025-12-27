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

# Begin Script
start_time = time.time()  # record start
print('----------------')
print('Code Start')
print('----------------')

## Create Time Elemenet


TimeElement = TimeModule.Time()
integrator_RK4 = IntegratorModels.RK4Integrator()

#=========================
## Create Primary Object
#=========================
Earth = ObjectModels.Earth()
Earth.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.ZeroAcceleration])
Earth.IntegratorProperties.integrator = integrator_RK4

#=========================
## Create Secondary Object
#=========================
Moon = ObjectModels.Moon()
Moon.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.PointMassGravity(Earth.PhysicalProperties.mu)])
Moon.IntegratorProperties.integrator = integrator_RK4

#=========================
## Create GEO Sat 
#=========================
GEOSatellite = ObjectModels.GEOSpaceVehicle()
GEOSatellite.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.PointMassGravity(Earth.PhysicalProperties.mu),
                                                                     ForceModels.nBodyGravity(Moon)])
GEOSatellite.IntegratorProperties.integrator = integrator_RK4

#=========================
## Create MEO Sat Object
#=========================
MEOSatellite = ObjectModels.MEOSpaceVehicle()
MEOSatellite.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.PointMassGravity(Earth.PhysicalProperties.mu),
                                                                     ForceModels.nBodyGravity(Moon)])
MEOSatellite.IntegratorProperties.integrator = integrator_RK4

#=========================
## Create LEO Sat Object
#=========================
LEOSatellite = ObjectModels.LEOSpaceVehicle()
LEOSatellite.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.PointMassGravity(Earth.PhysicalProperties.mu),
                                                                     ForceModels.nBodyGravity(Moon)])
LEOSatellite.IntegratorProperties.integrator = integrator_RK4

#=========================
## Create Lunar Sat Object
#=========================
LunarSatellite = ObjectModels.LunarSpaceVehicle()
LunarSatellite.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.PointMassGravity(Earth.PhysicalProperties.mu),
                                                                     ForceModels.nBodyGravity(Moon)])
LunarSatellite.IntegratorProperties.integrator = integrator_RK4

#=========================
## 2. Setup Propagator
#=========================
bodyList = [Earth, LEOSatellite, GEOSatellite, MEOSatellite, LunarSatellite, Moon]
PropagatorModels.Propagate(bodyList, TimeElement)



# Create a Color Scheme
Scheme = ColorSchemeObjects.VisualScheme_RetroMilitary()
Fig = StandardPlots.FigureObject(Scheme)

StandardPlots.Plot_Body(GEOSatellite)
StandardPlots.Plot_Body(MEOSatellite)
StandardPlots.Plot_Body(LEOSatellite)
StandardPlots.Plot_Body(LunarSatellite)
StandardPlots.Plot_Body(Moon)
StandardPlots.Plot_Body(Earth)

StandardPlots.Plot_Trajectory(LEOSatellite)
StandardPlots.Plot_Trajectory(GEOSatellite)
StandardPlots.Plot_Trajectory(MEOSatellite)
StandardPlots.Plot_Trajectory(LunarSatellite)
StandardPlots.Plot_Trajectory(Moon)

print('----------------')
print('Code End')
print('----------------')
end_time = time.time()    # record end
duration = end_time - start_time
print(f"Script runtime: {duration:.4f} seconds")





plt.show()


