import numpy as np
from typing import Optional
import ColorSchemeObjects as Color_Scheme

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
            self.position:          Optional[np.ndarray]    = None
            self.velocity:          Optional[np.ndarray]    = None
            self.stateHistory:      np.ndarray              = np.array([])
                
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
    
# Types of Propagators
class Propagator():
        def __init__(self):
            self.propagator_name            : Optional[str]         = None
            self.propagator_source          : Optional[str]         = None
            self.propagator_description     : Optional[str]         = None
            self.time_step                  : Optional[float]       = None
            self.abs_tolerance              : Optional[float]       = None
            self.rel_tolerance              : Optional[float]       = None 
            self.body_list                  : list[CelestialBody]   = []

class TwoBodyPropagator(Propagator):
    def __init__(self):
        super().__init__()
        self.propagator_name        = "Two-Body Propagator"
        self.propagator_source      = None
        self.propagator_description = "Propagates orbits using the two-body problem solution."
        self.time_step              = 60.0  # seconds
        self.abs_tolerance          = 1e-9
        self.rel_tolerance          = 1e-9
        self.primary                = self.body_list[0] if self.body_list else None 
        self.secondary              = self.body_list[1] if len(self.body_list) > 1 else None

    def Propagate(self, state_vector, time_span):
        # Placeholder for two-body propagation logic
        pass




