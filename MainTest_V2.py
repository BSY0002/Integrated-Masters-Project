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
import EphemerisModels

# Begin Script
start_time = time.time()  # record start
print('----------------')
print('Code Start')
print('----------------')

## Create Time Elemenet
TimeElement = TimeModule.Time()

## Create Objects
Moon = ObjectModels.Moon()
Earth = ObjectModels.Earth()
LEOSatellite = ObjectModels.LEOSpaceVehicle()
LEOSatelliteUnitTest = ObjectModels.LEOSpaceVehicle()

MEOSatellite = ObjectModels.MEOSpaceVehicle()
GEOSatellite = ObjectModels.GEOSpaceVehicle()
LunarSatellite = ObjectModels.LunarSpaceVehicle()

## Create Integrators
integrator_RK4 = IntegratorModels.RK4Integrator()
integrator_RK4Adaptive = IntegratorModels.AdaptiveRK4Integrator()
MoonEphemeris = IntegratorModels.EphemerisIntegrator(ephemeris_func = EphemerisModels.CircularEphemeris(body = Moon, centralBody = Earth))

#=========================
## Earth Properties
#=========================
Earth.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.Fixed])
Earth.IntegratorProperties.integrator = integrator_RK4
Earth.IntegratorProperties.dt = 1000

#=========================
## Moon Properties
#=========================
Moon.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.PointMassGravity(Earth)])
Moon.IntegratorProperties.integrator = MoonEphemeris
Moon.IntegratorProperties.dt = 1000

#=========================
## LEO Sat Properties
#=========================
def earth_density(h, t=None):
    # Simplified exponential model
    rho0 = 1.225       # kg/m^3 at sea level
    H = 8500.0         # scale height [m]
    return rho0 * np.exp(-h/H)

LEOSatellite.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.PointMassGravity(Earth),ForceModels.AtmosphericDrag(Cd=10.2, A=1000, mass=10000, radius=6371e3,omega=np.array([0, 0, 7.2921159e-5]), rho_func=earth_density, h_limit=2000e3)])
LEOSatellite.IntegratorProperties.integrator = integrator_RK4Adaptive
LEOSatellite.name = "LEO Pert"
LEOSatellite.VisualProperties.bodyColor = "#CC1100"
LEOSatellite.VisualProperties.lineColor = "#CC1100"
LEOSatellite.IntegratorProperties.dt = 1000

LEOSatelliteUnitTest.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.PointMassGravity(Earth)])
LEOSatelliteUnitTest.IntegratorProperties.integrator = integrator_RK4Adaptive
LEOSatelliteUnitTest.name = "LEO 2 Body"
LEOSatelliteUnitTest.IntegratorProperties.dt = 1000

#=========================
## GEO Sat Properties
#=========================
GEOSatellite.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.PointMassGravity(Earth),ForceModels.nBodyGravity(Moon)])
GEOSatellite.IntegratorProperties.integrator = integrator_RK4

#=========================
## MEO Sat Properties
#=========================
MEOSatellite.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.PointMassGravity(Earth),ForceModels.nBodyGravity(Moon)])
MEOSatellite.IntegratorProperties.integrator = integrator_RK4

#=========================
## Lunar Sat Properties
#=========================
LunarSatellite.IntegratorProperties.dynamics = IntegratorModels.Dynamics([ForceModels.PointMassGravity(Earth), ForceModels.nBodyGravity(Moon)])
LunarSatellite.IntegratorProperties.integrator = integrator_RK4Adaptive
LunarSatellite.IntegratorProperties.dt = 1000

#=========================
## Propagator
#=========================
bodyList = [Earth, LEOSatelliteUnitTest, LEOSatellite, GEOSatellite, MEOSatellite, LunarSatellite, Moon]
#bodyList = [Earth, LunarSatellite, Moon]
#bodyList = [Earth, Moon]
#bodyList = [Earth, LEOSatelliteUnitTest, LEOSatellite]
#bodyList = [Earth, LEOSatelliteUnitTest, LEOSatellite, LunarSatellite, Moon]
PropagatorModels.Propagate(bodyList, TimeElement)

#=========================
## Plotting
#=========================
# Create a Color Scheme
Scheme = ColorSchemeObjects.VisualScheme_RetroMilitary()
Fig = StandardPlots.FigureObject(Scheme)

AtmosCircle = Circle((0,0), Earth.PhysicalProperties.radius + 2000e3, edgecolor='red', facecolor='red', alpha = .1, linewidth=1)
EarthSurfaceCircle = Circle((0,0), Earth.PhysicalProperties.radius, edgecolor='blue', facecolor='blue', alpha = 1, linewidth=2)
Fig.ax.add_patch(AtmosCircle)
Fig.ax.add_patch(EarthSurfaceCircle)

for body in bodyList:
    StandardPlots.Plot_Body(body)
    StandardPlots.Plot_Trajectory(body)

end_time = time.time()
duration = end_time - start_time

for b in bodyList:
    print(
        b.name,
        "num states:", len(b.StateProperties.stateHistory),
        "time span:",
        b.StateProperties.times[0],
        "→",
        b.StateProperties.times[-1]
    )


print(max(Moon.StateProperties._times))
print(max(LEOSatellite.StateProperties._times))
print(max(LEOSatelliteUnitTest.StateProperties._times))

print(f"Script runtime: {duration:.4f} seconds")
Ani = StandardPlots.Animate_Trajectories(bodyList, Fig)
print('----------------')
print('Code End')
print('----------------')

plt.show()


