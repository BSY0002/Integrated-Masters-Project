import ForceModels
import IntegratorModels
import matplotlib.pyplot as plt
import RealTimePropagator
import numpy as np
import ExampleObjectClasses

plt.ion()

# ======================================
# Create bodies
# ======================================
Earth = ExampleObjectClasses.Earth()
LEOSatellite = ExampleObjectClasses.LEOSpaceVehicle()
AdvSatellite = ExampleObjectClasses.LEOSpaceVehicle()

# ======================================
# Integrators
# ======================================
integrator = IntegratorModels.AdaptiveRK45Integrator()

# ======================================
# Object Properties
# ======================================
# Earth
Earth.IntegratorProperties.orbit.dynamics = IntegratorModels.OrbitDynamics([ForceModels.Fixed])
Earth.IntegratorProperties.orbit.integrator = integrator

# LEO Sat
LEOSatellite.IntegratorProperties.orbit.dynamics = IntegratorModels.OrbitDynamics([ForceModels.PointMassGravity(Earth)])
LEOSatellite.IntegratorProperties.orbit.integrator = integrator
LEOSatellite.name = "LEOSat"

# Adv Sat
AdvSatellite.IntegratorProperties.orbit.dynamics = IntegratorModels.OrbitDynamics([ForceModels.PointMassGravity(Earth)])
AdvSatellite.IntegratorProperties.orbit.integrator = integrator
AdvSatellite.name = "AdvSat"
X = 6378137.0 + 20000000000
orbitState  = np.array([
                                            9378137,
                                            0.0,
                                            0.0,
                                            0.0,
                                            np.sqrt(3.986004418e14 / X),
                                            0.0])

AdvSatellite.StateProperties.set_orbitState(0, orbitState)
AdvSatellite.VisualProperties.bodyColor = "#CC1100"
AdvSatellite.VisualProperties.lineColor = "#CC1100"
AdvSatellite.VisualProperties.edgeColor = "#CC1100"


# ======================================
# Run
# ======================================
bodyList = [Earth, LEOSatellite, AdvSatellite]
rt = RealTimePropagator.RealTimePropagator(bodyList)
rt.RunRealTimeSimulation()

plt.show(block=True)
