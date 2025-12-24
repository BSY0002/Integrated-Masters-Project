import numpy as np

def Propagate(State, TimeElement, Integrator, Dynamics):
    state_history = State
    for time in TimeElement.timeVector:
        State = Integrator.step(deriv_func = Dynamics, 
                                state = State, 
                                time = time, 
                                dt = TimeElement.timeStep)
        state_history = np.vstack((state_history, State))
    return state_history
