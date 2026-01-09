import numpy as np

class Fixed:
    def accel(self, r=None, v=None, time=None):
        return np.zeros(3)
    def force(self, r=None, v=None, time=None):
        return np.zeros(3)
    
    
class PointMassGravity:
    def __init__(self, body):
        self.body = body

    def force(self, r, m, v=None, time=None):
        r_body = self.body.StateProperties.orbit_state_at_time(time)[0:3]
        r_rel  = r - r_body

        d = np.linalg.norm(r_rel)
        if d == 0.0:
            return np.zeros(3)

        return -m * self.body.PhysicalProperties.mu * r_rel / d**3
    
    def accel(self, r, v=None, time=None):
        r_body = self.body.StateProperties.orbit_state_at_time(time)[0:3]
        r_rel = r - r_body

        d = np.linalg.norm(r_rel)
        if d == 0.0:
            return np.zeros(3)

        return -self.body.PhysicalProperties.mu * r_rel / d**3

class NullTorque:
    def __init__(self):
        pass

    def torque(self, att_state=None, time=None):
        return np.zeros(3)
    
    def accel(self, att_state = None, time = None):
        return np.zeros(3)

