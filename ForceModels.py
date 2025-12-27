import numpy as np

class ZeroAcceleration:
    def accel(self, r=None, v=None, time=None):
        return np.zeros(3)

class PointMassGravity:
    def __init__(self, mu):
        self.mu = mu
        
    def accel(self, r, v=None, time=None):
        r_norm = np.linalg.norm(r)
        if r_norm == 0.0:
            return np.zeros(3)
        return -self.mu * r / r_norm**3
    
class nBodyGravity:
    def __init__(self, nBody):
        self.nBody = nBody  # position of the n-body

    def accel(self, r, v=None, time=None):
        #print(self.nBody.name)
        #print(self.nBody.StateProperties.stateCurrent[0:3])

        # relative position: spacecraft to third body
        r_sb = self.nBody.StateProperties.stateCurrent[0:3] - r
        d_sb = np.linalg.norm(r_sb)
        d_b = np.linalg.norm(self.nBody.StateProperties.stateCurrent[0:3])

        # third-body perturbation formula
        return self.nBody.PhysicalProperties.mu * (r_sb / d_sb**3 - self.nBody.StateProperties.stateCurrent[0:3] / d_b**3)
    
class J2Gravity:
    def __init__(self, CentralBody):
        self.mu = CentralBody.PhysicalProperties.mu
        self.radius = CentralBody.PhysicalProperties.radius
        self.J2 = CentralBody.PhysicalProperties.J2

    def accel(self, r, v=None, time=None):
        x, y, z = r
        r1 = np.linalg.norm(r)
        r5 = r1**5
        zx2 = (z / r1)**2

        factor = 1.5 * self.J2 * self.mu * self.radius**2 / r5

        return np.array([
            factor * x * (5*zx2 - 1),
            factor * y * (5*zx2 - 1),
            factor * z * (5*zx2 - 3),
        ])
    
def CombinedForces(forces, state, time):
    r = state[0:3]
    v = state[3:6]

    a_total = np.zeros(3)
    for force in forces:
        a_total += force.accel(r, v, time)  # only acceleration

    return np.hstack((v, a_total))
