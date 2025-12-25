## Unit Tests
import ForceModels 
import IntegratorModels
import TimeModule 
import numpy as np
import PropagatorModels

def TwoBodyPropagationTest():
    # THIS WILL BE DEFINED ELSE WHERE : Define State Elements
    r0 = np.array([6771e3, 0, 0])
    v0 = np.array([0, 7672.6, 0])    
    State = np.hstack((r0, v0))

    # THIS WILL BE DEFINED ELSE WHERE : Define Time Elements
    TimeElement = TimeModule.Time()

    # Define Constants
    mu_earth = 3.986004418e14

    # Define Forces
    pm = ForceModels.PointMassGravity(mu_earth)

    # Concatenate Forces
    Dynamics = IntegratorModels.Dynamics([pm])
    integrator_RK4 = IntegratorModels.RK4Integrator()

    StateHistory = PropagatorModels.Propagate(State, TimeElement, integrator_RK4, Dynamics)
    return StateHistory
