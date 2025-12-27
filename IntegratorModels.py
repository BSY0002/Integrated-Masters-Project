import numpy as np

class RK4Integrator:
    def step(self, deriv_func, state, time, dt):
        k1 = deriv_func(state, time)
        k2 = deriv_func(state + 0.5 * dt * k1, time + 0.5 * dt)
        k3 = deriv_func(state + 0.5 * dt * k2, time + 0.5 * dt)
        k4 = deriv_func(state + dt * k3, time + dt)
        new_state = state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        return new_state

class DOPRI5Integrator:
    def step(self, deriv_func, state, time, dt):
        k1 = deriv_func(state, time)

        k2 = deriv_func(
            state + dt * (1/5) * k1,
            time + dt * (1/5)
        )

        k3 = deriv_func(
            state + dt * ((3/40)*k1 + (9/40)*k2),
            time + dt * (3/10)
        )

        k4 = deriv_func(
            state + dt * ((44/45)*k1 - (56/15)*k2 + (32/9)*k3),
            time + dt * (4/5)
        )

        k5 = deriv_func(
            state + dt * ((19372/6561)*k1 - (25360/2187)*k2 +
                          (64448/6561)*k3 - (212/729)*k4),
            time + dt * (8/9)
        )

        k6 = deriv_func(
            state + dt * ((9017/3168)*k1 - (355/33)*k2 +
                          (46732/5247)*k3 + (49/176)*k4 -
                          (5103/18656)*k5),
            time + dt
        )

        # 5th-order Dormand–Prince solution
        new_state = state + dt * (
            (35/384)*k1 +
            (500/1113)*k3 +
            (125/192)*k4 -
            (2187/6784)*k5 +
            (11/84)*k6
        )

        return new_state

class Dynamics:
    def __init__(self, forces):
        self.forces = forces

    def __call__(self, state, time):
        if state.shape[0] != 6:
            raise ValueError("State vector must be length 6 [r, v]")

        r = state[0:3]
        v = state[3:6]
        a = np.zeros(3)
        
        for force in self.forces:
            a += force.accel(r, v, time)

        return np.hstack((v, a))