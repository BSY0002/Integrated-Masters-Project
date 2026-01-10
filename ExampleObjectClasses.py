import ObjectModels
import numpy as np

# =======================================================
# Planetary Bodies
# =======================================================
class Earth(ObjectModels.Planet):
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

class Moon(ObjectModels.Planet):
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


# =======================================================
# Spacecraft
# =======================================================
class LunarSpaceVehicle(ObjectModels.SpaceVehicle):
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
        
class LEOSpaceVehicle(ObjectModels.SpaceVehicle):
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
