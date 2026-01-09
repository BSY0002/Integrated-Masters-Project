import numpy as np

class RK4Integrator():
    def step(self, deriv_func, state, time, dt):
        k1 = deriv_func(state, time)
        k2 = deriv_func(state + 0.5 * dt * k1, time + 0.5 * dt)
        k3 = deriv_func(state + 0.5 * dt * k2, time + 0.5 * dt)
        k4 = deriv_func(state + dt * k3, time + dt)
        new_state = state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        return new_state

class AdaptiveRK45Integrator():
    """
    Adaptive Runge-Kutta 4(5) integrator (Dormand-Prince)
    Compatible with: step(deriv_func, state, t, dt, absTol, relTol)
    """
    # Dormand-Prince coefficients
    c = np.array([0, 1/5, 3/10, 4/5, 8/9, 1, 1])
    a = [
        [],
        [1/5],
        [3/40, 9/40],
        [44/45, -56/15, 32/9],
        [19372/6561, -25360/2187, 64448/6561, -212/729],
        [9017/3168, -355/33, 46732/5247, 49/176, -5103/18656],
        [35/384, 0, 500/1113, 125/192, -2187/6784, 11/84]
    ]
    b5 = np.array([35/384, 0, 500/1113, 125/192, -2187/6784, 11/84, 0])  # 5th order
    b4 = np.array([5179/57600, 0, 7571/16695, 393/640, -92097/339200, 187/2100, 1/40])  # 4th order

    def step(self, deriv_func, state, t, dt, absTol=1e-12, relTol=1e-12):
        k = []
        # Compute k1..k7
        k1 = deriv_func(state, t)
        k.append(k1)
        k2 = deriv_func(state + dt*(self.a[1][0]*k[0]), t + self.c[1]*dt)
        k.append(k2)
        k3 = deriv_func(state + dt*(self.a[2][0]*k[0] + self.a[2][1]*k[1]), t + self.c[2]*dt)
        k.append(k3)
        k4 = deriv_func(state + dt*(self.a[3][0]*k[0] + self.a[3][1]*k[1] + self.a[3][2]*k[2]), t + self.c[3]*dt)
        k.append(k4)
        k5 = deriv_func(state + dt*(self.a[4][0]*k[0] + self.a[4][1]*k[1] + self.a[4][2]*k[2] + self.a[4][3]*k[3]), t + self.c[4]*dt)
        k.append(k5)
        k6 = deriv_func(state + dt*(self.a[5][0]*k[0] + self.a[5][1]*k[1] + self.a[5][2]*k[2] + self.a[5][3]*k[3] + self.a[5][4]*k[4]), t + self.c[5]*dt)
        k.append(k6)
        k7 = deriv_func(state + dt*(self.a[6][0]*k[0] + self.a[6][1]*k[1] + self.a[6][2]*k[2] + self.a[6][3]*k[3] + self.a[6][4]*k[4] + self.a[6][5]*k[5]), t + self.c[6]*dt)
        k.append(k7)

        # 5th-order solution
        x5 = state + dt * sum(bi*ki for bi, ki in zip(self.b5, k))
        # 4th-order embedded solution
        x4 = state + dt * sum(bi*ki for bi, ki in zip(self.b4, k))

        # Error estimate
        err = np.linalg.norm(x5 - x4)
        tol = absTol + relTol * np.linalg.norm(x5)

        return x5, err, tol

class EphemerisIntegrator():
    def __init__(self, ephemeris_func):
        self.ephemeris_func = ephemeris_func

    def step(self, deriv_func, state, time, dt):
        return self.ephemeris_func(time + dt)

class OrbitDynamics:
    def __init__(self, forces):
        self.forces = forces

    def __call__(self, state, time):
        # state = [x y z vx vy vz]
        r = state[0:3]
        v = state[3:6]

        a = np.zeros(3)
        for force in self.forces:
            a += force.accel(r, v, time)

        dxdt = np.zeros(6)
        dxdt[0:3] = v
        dxdt[3:6] = a

        return dxdt
    
class AttitudeDynamics:
    def __init__(self, torques, body):
        """
        Parameters:
        torques : list
            List of torque objects with method torque(att_state, time)
        inertia : np.array, shape (3,3)
            Inertia tensor of the body in body frame
        """
        self.torques = torques
        self.body = body
        self.inertia = self.body.PhysicalProperties.inertia

    @staticmethod
    def quat_omega_matrix(w):
        wx, wy, wz = w
        return np.array([
            [ 0, -wx, -wy, -wz],
            [wx,  0,  wz, -wy],
            [wy, -wz,  0,  wx],
            [wz,  wy, -wx,  0],
        ])

    def __call__(self, state, time):
        """
        Compute state derivative for [q0 q1 q2 q3 wx wy wz]
        
        Parameters:
        state : np.array, shape (7,)
            Attitude quaternion and angular velocity
        time : float
            Current simulation time
        
        Returns:
        dxdt : np.array, shape (7,)
            Derivative of state
        """
        q = state[0:4]  # quaternion

        w = state[4:7]  # angular velocity

        # Quaternion kinematics
        q_dot = 0.5 * self.quat_omega_matrix(w) @ q

        # Sum all torques (each torque only depends on att_state and time)
        torque_total = np.zeros(3)
        for T in self.torques:
            torque_total += T.torque(att_state=q, time=time)

        # Angular acceleration: α = I⁻¹ (τ - ω × (I ω))
        w_dot = np.linalg.solve(self.inertia, torque_total - np.cross(w, self.inertia @ w))

        # Pack derivative
        dxdt = np.zeros(7)
        dxdt[0:4] = q_dot
        dxdt[4:7] = w_dot
        return dxdt
