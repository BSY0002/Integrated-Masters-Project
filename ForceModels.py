import numpy as np

class PointMassGravity:
    def __init__(self, mu):
        self.mu = mu

    def dxdt(self, state, time=None):
        r = state[0:3]  
        v = state[3:6]
        norm_r = np.linalg.norm(r)
        a = -self.mu * r / norm_r**3
        dxdt = np.hstack((v, a))
        return dxdt

class J2Gravity:
    def __init__(self, mu, radius, J2):
        self.mu = mu
        self.radius = radius
        self.J2 = J2

    def dxdt(self, state, time=None):
        r = state[0:3]
        v = state[3:6]

        x, y, z = r
        r2 = np.dot(r, r)
        r1 = np.sqrt(r2)
        r5 = r1**5

        zx2 = (z / r1)**2

        factor = (3/2) * self.J2 * self.mu * self.radius**2 / r5

        ax = factor * x * (5*zx2 - 1)
        ay = factor * y * (5*zx2 - 1)
        az = factor * z * (5*zx2 - 3)

        a = np.array([ax, ay, az])

        dxdt = np.hstack((v, a))
        return dxdt

def CombinedForces(forces, state, time):
    dxdt = np.zeros_like(state)
    for force in forces:
        dxdt += force.dxdt(state, time)
    return dxdt