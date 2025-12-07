import numpy as np
from typing import Optional
import ColorSchemeObjects as Color_Scheme
import CommonParameterObjects as CommonParameters

class GeneralObject:
    def __init__(self, name : str):
        self.name : str = name
        self.description : Optional[str] = None

# System Object 
class SystemObject(GeneralObject):
    def __init__(self, name):
        super().__init__(name)
        self.child_objects: list[GeneralObject] = []

# Types of Bodies
class CelestialBody(GeneralObject):
    def __init__(self, name):
        super().__init__(name)
        self.keplarian_properties       = self.KeplarianProperties()
        self.state_properties           = self.StateProperties()
        self.osculating_properties      = self.OsculatingProperties()
        self.physical_properties        = self.PhysicalProperties()
        self.visual_properties          = self.VisualProperties(Color_Scheme.ColorScheme.VisualScheme_Default.Primary)

    class KeplarianProperties:
        def __init__(self):
            self.semi_major_axis:                   Optional[float] = None
            self.eccentricity:                      Optional[float] = None
            self.inclination:                       Optional[float] = None
            self.longitude_of_ascending_node:       Optional[float] = None
            self.argument_of_periapsis:             Optional[float] = None
            self.mean_anomaly:                      Optional[float] = None
                
    class StateProperties:
        def __init__(self):
            self.position:          np.ndarray              = np.array([])
            self.velocity:          np.ndarray              = np.array([])
            self.stateHistory:      np.ndarray              = np.array([])
            self.timeHistory:       np.ndarray              = np.array([])
        
        @property
        def currentStateVector(self):
            if self.position.any() is None:
                return None
            if self.velocity.any() is None:
                return None
            return np.concat([self.position, self.velocity])
    
    class OsculatingProperties:
        def __init__(self):
            self.semi_major_axis: Optional[float] = None
            self.eccentricity: Optional[float] = None
            self.inclination: Optional[float] = None
            self.longitude_of_ascending_node: Optional[float] = None
            self.argument_of_periapsis: Optional[float] = None
            self.mean_anomaly: Optional[float] = None

    class PhysicalProperties:
        def __init__(self):
            self.mass: Optional[float] = None
            self.radius: Optional[float] = None

        @property
        def mu(self):
            if self.mass is None: 
                raise ValueError("Unset Value Error")
            return self.mass * CommonParameters.G.parameter_value
    
    class VisualProperties:
        def __init__(self, ColorScheme):
            self.bodyColor  : Optional[str]   = ColorScheme.bodyColor
            self.edgeColor  : Optional[str]   = ColorScheme.edgeColor
            self.lineWidth  : Optional[float] = ColorScheme.lineWidth
            self.lineColor  : Optional[str]   = ColorScheme.lineColor
            self.size       : Optional[float] = ColorScheme.size
            self.icon       : Optional[str]   = ColorScheme.icon

        def setColorScheme(self, ColorScheme):
            self.bodyColor  = ColorScheme.bodyColor
            self.edgeColor  = ColorScheme.edgeColor
            self.lineColor  = ColorScheme.lineColor
            self.lineWidth  = ColorScheme.lineWidth
            self.size       = ColorScheme.size
            self.icon       = ColorScheme.icon

class Planet(CelestialBody):
    def __init__(self, name):
        super().__init__(name)

class SpaceVehicle(CelestialBody):
    def __init__(self, name):
        super().__init__(name)
    





