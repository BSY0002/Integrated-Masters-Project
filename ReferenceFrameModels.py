import numpy as np

class ReferenceFrame:
    def transform_state(self, state, time):
        raise NotImplementedError
    
class BodyCenteredInertialFrame(ReferenceFrame):
    def __init__(self, body):
        self.body = body

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

def apply_frames(state, time, frames):
    for frame in frames:
        state = frame.transform_state(state, time)
    return state

def Rz(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [ c, -s, 0],
        [ s,  c, 0],
        [ 0,  0, 1]
    ])
