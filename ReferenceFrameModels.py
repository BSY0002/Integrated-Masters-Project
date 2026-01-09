import numpy as np

## Reference Frames
class ReferenceFrame:
    def __init__(self):
        self.name = "Default Frame"
        self.iFrame = np.array([1,0,0])
        self.jFrame = np.array([0,1,0])
        self.jFrame = np.array([0,0,1])
        
    def transform_state(self, state, time):
        raise NotImplementedError
    
class BodyCenteredInertialFrame(ReferenceFrame):
    def __init__(self, body):
        self.body = body
        self.iFrame = np.array([1,0,0])
        self.jFrame = np.array([0,1,0])
        self.jFrame = np.array([0,0,1])
        

    def transform_state(self, state, time):
        r = state[0:3]
        v = state[3:6]

        r_body = self.body.StateProperties.state_at_time(time)[0:3]
        v_body = self.body.StateProperties.state_at_time(time)[3:6]

        r_new = r - r_body
        v_new = v - v_body


        return np.hstack((r_new, v_new))

class BodyFixedFrame(ReferenceFrame):
    def __init__(self, body, omega):
        self.body = body
        self.omega = np.asarray(omega)

    def transform_state(self, state, time):
        r = state[0:3]
        v = state[3:6]

        body_state = self.body.StateProperties.state_at_time(time)
        r_body = body_state[0:3]
        v_body = body_state[3:6]

        # Relative to body
        r_rel = r - r_body
        v_rel = v - v_body

        # Rotation
        theta = np.linalg.norm(self.omega) * time
        R = Rz(theta)

        r_rot = R @ r_rel

        # Velocity in rotating frame
        v_rot = R @ (v_rel - np.cross(self.omega, r_rel))

        return np.hstack((r_rot, v_rot))

class TwoBodySynodicFrame(ReferenceFrame):
    def __init__(self, primary, secondary):
        """
        Generic rotating synodic frame for two bodies.
        primary, secondary: body objects
        omega_vector: rotation vector (3,) in rad/s (e.g., [0,0,omega] for z-axis rotation)
        """
        self.primary = primary
        self.secondary = secondary
        self.omega = np.asarray(np.array([0, 0, 2*np.pi / (secondary.StateProperties.Period)]))  # rad/s

    def barycenter(self, time):
        """Compute the center of mass of the two bodies at the given time."""
        r1 = self.primary.StateProperties.state_at_time(time)[0:3]
        r2 = self.secondary.StateProperties.state_at_time(time)[0:3]
        m1 = self.primary.PhysicalProperties.mass
        m2 = self.secondary.PhysicalProperties.mass
        return (m1 * r1 + m2 * r2) / (m1 + m2)

    def transform_state(self, state, time):
        r = state[0:3]
        v = state[3:6]

        # Position relative to barycenter
        r_bary = self.barycenter(time)
        r_rel = r - r_bary
        
        # Rotation matrix from angular velocity vector
        theta = np.linalg.norm(self.omega) * time
        R = Rz(theta)  # For general rotation, could use Rodrigues formula

        # Rotate position
        r_rot = R @ r_rel

        # Velocity in rotating frame
        v1 = self.primary.StateProperties.state_at_time(time)[3:6]
        v2 = self.secondary.StateProperties.state_at_time(time)[3:6]
        v_bary = (self.primary.PhysicalProperties.mass * v1 + self.secondary.PhysicalProperties.mass * v2) / (self.primary.PhysicalProperties.mass + self.secondary.PhysicalProperties.mass)

        v_rel = v - v_bary
        v_rot = R @ (v_rel - np.cross(self.omega, r_rel))

        return np.hstack((r_rot, v_rot))













## Methods
def apply_frames(state, time, frames):
    for frame in frames:
        state = frame.transform_state(state, time)
    return state

def Rx(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s,  c]
    ])

def Ry(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [ c, 0, s],
        [ 0, 1, 0],
        [-s, 0, c]
    ])

def Rz(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [ c, -s, 0],
        [ s,  c, 0],
        [ 0,  0, 1]
    ])