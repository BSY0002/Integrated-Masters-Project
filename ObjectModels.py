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
        self.PhysicalProperties.mu = 3.986004418e14  # m^3 / s^2
        self.PhysicalProperties.J2 = 1.08262668e-3
        self.PhysicalProperties.mass = 5.972e24
        self.PhysicalProperties.radius = 6371.0

        ## Set the State Properties ##
        self.StateProperties.position = np.array([0, 0, 0])
        self.StateProperties.velocity = np.array([0, 0, 0])
        self.StateProperties.acceleration = np.array([0, 0, 0])

        ## Set the Visual Properties ##

## Specific Object Classes ##
class Moon(Planet):
    def __init__(self):
        super().__init__(name="Moon")
        ## Set the Physical Properties (Moon) ##
        self.PhysicalProperties.mu     = 4.9048695e12   # m^3 / s^2
        self.PhysicalProperties.J2     = 2.03263e-4
        self.PhysicalProperties.mass   = 7.342e22       # kg
        self.PhysicalProperties.radius = 1737.4         # km

        ## Set the State Properties (Moon relative to Earth, ECI) ##
        # Mean distance and velocity, circular orbit assumption
        self.StateProperties.position = np.array([
            384400e3,   # x [m]
            0.0,        # y [m]
            0.0         # z [m]
        ])

        self.StateProperties.velocity = np.array([
            0.0,        # vx [m/s]
            1022.0,     # vy [m/s]
            0.0         # vz [m/s]
        ])

        self.StateProperties.acceleration = np.array([0.0, 0.0, 0.0])

class TestSpaceVehicle(SpaceVehicle):
    def __init__(self):
        super().__init__(name="TestSpaceVehicle")
        self.StateProperties.position = np.array([7000e3, 0, 0]) 
        self.StateProperties.velocity = np.array([0, 7500, 0])

## Standard Property Set Classes ##
class PhysicalProperties():
    def __init__(self):
        self.J2 = 0.0
        self.mass = 0.0
        self.radius = 0.0
        self.mu = 0.0
        pass

class VisualProperties():
    def __init__(self):
        pass

class StateProperties():
    def __init__(self):
        self.position       = np.array([])
        self.velocity       = np.array([])
        self.acceleration   = np.array([])
        self.positionHistory = np.array([])
        self.velocityHistory = np.array([])
        self.accelerationHistory = np.array([])
        self.stateHistory = np.array([])
    
    @property
    def state(self):
        return np.hstack((self.position, self.velocity))
