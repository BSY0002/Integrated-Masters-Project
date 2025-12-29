from typing import Optional
import IntegratorModels

import numpy as np

## Standard Object Classes ##
class GeneralObject:
    def __init__(self, name : str):
        self.name : str = name
        self.description : Optional[str] = None
        
## Celestial Body Classes ##
class CelestialBody(GeneralObject):
    def __init__(self, name):
        super().__init__(name)
        self.StateProperties = StateProperties()
        self.PhysicalProperties = PhysicalProperties()
        self.VisualProperties = VisualProperties()
        self.IntegratorProperties = IntegratorProperties()

class SpaceVehicle(CelestialBody):
    def __init__(self, name : str):
        super().__init__(name)

class Planet(CelestialBody):
    def __init__(self, name : str):
        super().__init__(name)

## Specific Object Classes ##
class Earth(Planet):
    def __init__(self):
        super().__init__(name="Earth")

        ## Set the Physical Properties ##
        self.PhysicalProperties.mu     = 3.986004418e14   # m^3 / s^2 (GM)
        self.PhysicalProperties.J2     = 1.08262668e-3    # dimensionless
        self.PhysicalProperties.mass   = 5.9722e24        # kg
        self.PhysicalProperties.radius = 6378137.0        # m (equatorial radius, WGS-84)
        self.SOI  = 9.24e8    # meters

        ## Set the State Properties ##
        state = np.array([0,0,0,0,0,0])
        
        # Set initial state
        self.StateProperties.set_state(0, state)

        ## Set the Visual Properties ##
        self.VisualProperties.bodyColor   = "#1313C9"
        self.VisualProperties.edgeColor   = "#000000"
        self.VisualProperties.lineColor   = "#1313C9"
        self.VisualProperties.textColor   = "#1313C9"
        self.VisualProperties.size        = 500

## Specific Object Classes ##
class Moon(Planet):
    def __init__(self):
        super().__init__(name="Moon")

        ## Physical Properties ##
        self.PhysicalProperties.mu     = 4.9048695e12   # m^3 / s^2
        self.PhysicalProperties.J2     = 2.03263e-4
        self.PhysicalProperties.mass   = 7.342e22       # kg
        self.PhysicalProperties.radius = 1737.4e3       # m
        self.SOI  = 6.61e7    # meters

        ## State Properties (Earth-centered inertial frame) ##
        # Moon at average distance from Earth
        state = np.array([
            384400e3, 0.0, 0.0,   # x, y, z position (m)
            0.0, 1022.0, 0.0       # vx, vy, vz velocity (m/s)
        ])

        # Set initial state
        self.StateProperties.set_state(0, state)

        ## Set the Visual Properties (Moon) ##
        self.VisualProperties.bodyColor   = "#888888"
        self.VisualProperties.edgeColor   = "#000000"
        self.VisualProperties.lineColor   = "#888888"
        self.VisualProperties.textColor   = "#888888"
        self.VisualProperties.lineWidth   = 1
        self.VisualProperties.size        = 300

class LunarSpaceVehicle(SpaceVehicle):
    def __init__(self):
        super().__init__(name="LunarSpaceVehicle")

        ## State Properties (Earth-centered inertial frame) ##
        # 10,000 km behind Moon toward Earth
        state = np.array([
                                386237000.0+10000000, 0.0, 0.0,   # position (m)
                                0.0, 1500, 0.0           # velocity (m/s)
                                ])
        
        # Set initial state
        self.StateProperties.set_state(0, state)

        ## Set the Visual Properties ##
        self.VisualProperties.bodyColor   = "#000000"
        self.VisualProperties.edgeColor   = "#4aff00"
        self.VisualProperties.lineColor   = "#4aff00"
        self.VisualProperties.textColor   = "#4aff00"
        self.VisualProperties.size        = 15
        self.VisualProperties.icon        = '>'
        
class LEOSpaceVehicle(SpaceVehicle):
    def __init__(self):
        super().__init__(name="LEOSpaceVehicle")

        ## State Properties (Earth-centered inertial frame) ##
        X = 6378137.0 + 150000
        state  = np.array([
                                            X,
                                            0.0,
                                            0.0,
                                            0.0,
                                            np.sqrt(3.986004418e14 / X),
                                            0.0
                                        ])
        # Set initial state
        self.StateProperties.set_state(0, state)

        ## Set the Visual Properties ##
        self.VisualProperties.bodyColor   = "#000000"
        self.VisualProperties.edgeColor   = "#4aff00"
        self.VisualProperties.lineColor   = "#4aff00"
        self.VisualProperties.textColor   = "#4aff00"
        self.VisualProperties.size        = 15
        self.VisualProperties.icon        = '>'

class MEOSpaceVehicle(SpaceVehicle):
    def __init__(self):
        super().__init__(name="MEOSpaceVehicle")

        ## State Properties (Earth-centered inertial frame) ##
        # 10,000 km behind Moon toward Earth
        state = np.array([
                                    26578137.0,
                                    0.0,
                                    0.0,
                                    0.0,
                                    3873.957505,
                                    0.0
                                ])
        # Set initial state
        self.StateProperties.set_state(0, state)

        ## Set the Visual Properties ##
        self.VisualProperties.bodyColor   = "#000000"
        self.VisualProperties.edgeColor   = "#4aff00"
        self.VisualProperties.lineColor   = "#4aff00"
        self.VisualProperties.textColor   = "#4aff00"
        self.VisualProperties.size        = 15
        self.VisualProperties.icon        = '>'

class GEOSpaceVehicle(SpaceVehicle):
    def __init__(self):
        super().__init__(name="GEOSpaceVehicle")

        ## State Properties (Earth-centered inertial frame) ##
        # 10,000 km behind Moon toward Earth
        state = np.array([
                                            42164137.0,
                                            0.0,
                                            0.0,
                                            0.0,
                                            3074.661312,
                                            0.0
                                        ])
        # Set initial state
        self.StateProperties.set_state(0, state)

        ## Set the Visual Properties ##
        self.VisualProperties.bodyColor   = "#000000"
        self.VisualProperties.edgeColor   = "#4aff00"
        self.VisualProperties.lineColor   = "#4aff00"
        self.VisualProperties.textColor   = "#4aff00"
        self.VisualProperties.size        = 15
        self.VisualProperties.icon        = '>'

## Standard Property Set Classes ##
class PhysicalProperties:
    def __init__(self):
        self.J2 = 0.0
        self.mass = 0.0
        self.radius = 0.0
        self.mu = 0.0
        self.SOI = 0.0

class VisualProperties:
    def __init__(self):
        self.bodyColor = "#000000"
        self.edgeColor = "#CC1100"
        self.lineColor = "#CC1100"
        self.textColor = "#CC1100"
        self.lineWidth = .25
        self.size = 500
        self.icon = '.'

class StateProperties:
    def __init__(self):
        self._times = []
        self._states = []
        self._stateCurrent = None

    @property
    def stateCurrent(self):
        return self._stateCurrent

    @property
    def times(self):
        return np.asarray(self._times)

    @property
    def stateHistory(self):
        return np.vstack(self._states)

    @property
    def latest_time(self):
        if not self._times:
            return None
        return self._times[-1]

    def set_state(self, time, state):
        state = np.asarray(state, dtype=float)

        # enforce monotonic time
        if self._times and time <= self._times[-1]:
            return

        self._times.append(float(time))
        self._states.append(state.copy())
        self._stateCurrent = state

    def state_at_time(self, t):
        times = self.times
        states = self.stateHistory

        if t <= times[0]:
            return states[0]

        if t >= times[-1]:
            return states[-1]

        i = np.searchsorted(times, t) - 1
        t0, t1 = times[i], times[i + 1]
        s0, s1 = states[i], states[i + 1]

        alpha = (t - t0) / (t1 - t0)
        return (1 - alpha) * s0 + alpha * s1


class IntegratorProperties:
    def __init__(self):
        self.integrator = IntegratorModels.baseIntegrator()
        self.dynamics   = IntegratorModels.baseDynamics()

        self.absTol = 1e-6
        self.relTol = 1e-6

        self.dt      = 10.0     # current step
        self.dt_min  = .01
        self.dt_max  = 3600.0

    @property
    def is_propagated(self):
        return self.integrator is not None and self.dynamics is not None
