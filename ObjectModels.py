from typing import Optional
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
        self.IntegratorProperties = BodyIntegratorProperties()

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
        orbitState = np.array([0,0,0,0,0,0])
        attitudeState = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.2921159e-5])
        #7.2921159e-5
        # Set initial state
        self.StateProperties.set_attitudeState(0,attitudeState)
        self.StateProperties.set_orbitState(0, orbitState)
        
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
        orbitState = np.array([
            384400e3, 0.0, 0.0,   # x, y, z position (m)
            0.0, 1022.0, 0.0       # vx, vy, vz velocity (m/s)
        ])

        # Set initial state
        self.StateProperties.set_orbitState(0, orbitState)

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
        orbitState = np.array([
                                386237000.0+10000000, 0.0, 0.0,   # position (m)
                                0.0, 1500, 0.0           # velocity (m/s)
                                ])
        orbitState = np.array([
        4.57e7,     # x  (m)
        -6.14e6,     # y  (m)
        0.0,        # z  (m)
        4.90e2,     # vx (m/s)
        3.65e3,     # vy (m/s)
        0.0         # vz (m/s)
        ])
        # Set initial state
        self.StateProperties.set_orbitState(0, orbitState)

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
        orbitState  = np.array([
                                            X,
                                            0.0,
                                            0.0,
                                            0.0,
                                            np.sqrt(3.986004418e14 / X),
                                            0.0
                                        ])
        attitudeState = np.array([1.0, 0.0, 0.0, 0.0, 0, 0, 5E-2])

        # Set initial state
        self.StateProperties.set_orbitState(0, orbitState)
        self.StateProperties.set_attitudeState(0, attitudeState)

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
        orbitState = np.array([
                                    26578137.0,
                                    0.0,
                                    0.0,
                                    0.0,
                                    3873.957505,
                                    0.0
                                ])
        # Set initial state
        self.StateProperties.set_orbitState(0, orbitState)

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
        orbitState = np.array([
                                            42164137.0,
                                            0.0,
                                            0.0,
                                            0.0,
                                            3074.661312,
                                            0.0
                                        ])
        # Set initial state
        self.StateProperties.set_orbitState(0, orbitState)

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
        self.inertia = np.array([[1.0, 0.,   0.,  ],
                                [0.,   1.0, 0.  ],
                                [0.,   0.,   1.0]])

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
        
        # Time - As of right now, this should be the same for att and orbit states
        # ignore the above statement, need to split into seperate times
        #self._times = []
        self._attitude_times = []
        self._orbit_times = []

        # Orbit States - [x y z dx dy dz]
        self._orbit_states = [] 
        self._orbit_stateCurrent = None

        # Attitude States - [q0 q1 q2 q3 wx wy wz]
        self._attitude_states = []   
        self._attitude_stateCurrent = None

## ORBIT STATE
    @property
    def orbit_latest_time(self):
        return self._orbit_times[-1]
    
    @property
    def orbit_times(self):
        return np.asarray(self._orbit_times)


    @property
    def orbit_stateCurrent(self):
        return self._orbit_stateCurrent

    @property
    def orbit_stateHistory(self):
        return np.vstack(self._orbit_states)
    
    def set_orbitState(self, time, orbitState):
        
        orbitState = np.asarray(orbitState, dtype=float)

        # enforce monotonic time
        if self._orbit_times and time <= self._orbit_times[-1]:
            return

        self._orbit_times.append(float(time))
        self._orbit_states.append(orbitState.copy())
        self._orbit_stateCurrent = orbitState

    def orbit_state_at_time(self, t):
        if not self._orbit_times:
            return None

        times = self.orbit_times
        orbitStates = self.orbit_stateHistory

        if t <= times[0]:
            return orbitStates[0]

        if t >= times[-1]:
            return orbitStates[-1]

        i = np.searchsorted(times, t) - 1
        t0, t1 = times[i], times[i + 1]
        s0, s1 = orbitStates[i], orbitStates[i + 1]

        alpha = (t - t0) / (t1 - t0)
        return (1 - alpha) * s0 + alpha * s1

## ATTITUDE STATE
    @property
    def attitude_latest_time(self):
        if not self._attitude_times:
            return None
        return self._attitude_times[-1]
    
    @property
    def attitude_times(self):
        return np.asarray(self._attitude_times)



    @property
    def attitude_stateCurrent(self):
        return self._attitude_stateCurrent

    @property
    def attitude_stateHistory(self):
        return np.vstack(self._attitude_states)
    
    def set_attitudeState(self, time, attitudeState):
        attitudeState = np.asarray(attitudeState, dtype=float)
        if self._attitude_times and time <= self._attitude_times[-1]:
            return
        self._attitude_times.append(float(time))
        self._attitude_states.append(attitudeState.copy())
        self._attitude_stateCurrent = attitudeState

    def attitude_state_at_time(self, t):

        if not self._attitude_times:
            return None
        times = self.orbit_times
        attitudeStates = self.attitude_stateHistory

        if t <= times[0]:
            return attitudeStates[0]

        if t >= times[-1]:
            return attitudeStates[-1]

        i = np.searchsorted(times, t) - 1
        t0, t1 = times[i], times[i + 1]
        s0, s1 = attitudeStates[i], attitudeStates[i + 1]

        alpha = (t - t0) / (t1 - t0)
        return (1 - alpha) * s0 + alpha * s1

class BodyIntegratorProperties:
    def __init__(self):
        self.orbit    = IndividualIntegratorProperties()
        self.attitude = IndividualIntegratorProperties()

        # synchronization cadence (physical time)
        self.sync_dt = 1

class IndividualIntegratorProperties:
    def __init__(self):
        self.integrator: Optional[object] = None
        self.dynamics: Optional[object] = None

        self.absTol = 1e-12
        self.relTol = 1e-12

        self.dt      = 10     # current step
        self.dt_min  = .01
        self.dt_max  = 1000

    @property
    def is_propagated(self):
        return self.integrator is not None and self.dynamics is not None
    