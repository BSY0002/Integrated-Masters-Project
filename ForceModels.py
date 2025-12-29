import numpy as np

class Fixed:
    def accel(self, r=None, v=None, time=None):
        return np.zeros(3)

class PointMassGravity:
    def __init__(self, body):
        self.body = body

    def accel(self, r, v=None, time=None):
        r_body = self.body.StateProperties.state_at_time(time)[0:3]
        r_rel = r - r_body

        d = np.linalg.norm(r_rel)
        if d == 0.0:
            return np.zeros(3)

        return -self.body.PhysicalProperties.mu * r_rel / d**3

class nBodyGravity:
    def __init__(self, nBody):
        self.nBody = nBody

    def accel(self, r, v=None, time=None):
        # Get n-body position AT THE SAME TIME
        r_body = self.nBody.StateProperties.state_at_time(time)[0:3]

        # Spacecraft relative to n-body
        r_sb = r_body - r
        d_sb = np.linalg.norm(r_sb)
        d_b  = np.linalg.norm(r_body)

        if d_sb == 0.0 or d_b == 0.0:
            return np.zeros(3)

        mu = self.nBody.PhysicalProperties.mu

        return mu * (
            r_sb / d_sb**3
            - r_body / d_b**3
        )

class J2:
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
    
class AtmosphericDrag:
    def __init__(self, Cd, A, mass, radius, omega=np.zeros(3), rho_func=None, h_limit=1000e3):
        """
        Cd      : Drag coefficient
        A       : Cross-sectional area of spacecraft
        mass    : Spacecraft mass
        radius  : Planet radius [m]
        omega   : Planet rotation vector [rad/s], default zero
        rho_func: Function rho(h, time) returning atmospheric density at altitude h
        h_limit : Altitude above which drag is negligible
        """
        self.Cd = Cd
        self.A = A
        self.mass = mass
        self.radius = radius
        self.omega = omega
        self.rho_func = rho_func if rho_func is not None else (lambda h, t: 0.0)
        self.h_limit = h_limit

    def accel(self, r, v, time=None):
        h = np.linalg.norm(r) - self.radius
        if h > self.h_limit:  # above atmosphere, negligible drag
            return np.zeros(3)

        # relative velocity to rotating atmosphere
        v_rel = v - np.cross(self.omega, r)
        v_norm = np.linalg.norm(v_rel)

        rho = self.rho_func(h, time)
        return -0.5 * rho * self.Cd * self.A / self.mass * v_norm * v_rel

def CombinedForces(forces, state, time):
    r = state[0:3]
    v = state[3:6]

    a_total = np.zeros(3)
    for force in forces:
        a_total += force.accel(r, v, time)  # only acceleration

    return np.hstack((v, a_total))



