from typing import Optional
import CommonObjects as CommonObjects
import numpy as np
from scipy.integrate import solve_ivp
import CommonParameterObjects as CommonParameter


# Types of Propagators
class Propagator():
        def __init__(self):
            self.propagator_name            : Optional[str]         = None
            self.propagator_source          : Optional[str]         = None
            self.propagator_description     : Optional[str]         = None
            self.time_step                  : Optional[float]       = None
            self.abs_tolerance              : Optional[float]       = None
            self.rel_tolerance              : Optional[float]       = None 
            self.body_list                  : list[CommonObjects.CelestialBody]   = []

class TwoBodyPropagator(Propagator):
    def __init__(self):
        super().__init__()
        self.propagator_name        = "Two-Body Propagator"
        self.propagator_source      = None
        self.propagator_description = "Propagates orbits using the two-body problem solution."
        self.time_step              = 60.0  # seconds
        self.abs_tolerance          = 1e-9
        self.rel_tolerance          = 1e-9
        self.time_vector            = np.array([])

    @property
    def primary(self):
        return self.body_list[0]
    
    @property
    def secondary(self):
        return self.body_list[1]

    def Propagate(self):
            mu              = self.primary.physical_properties.mu
            state_vector    = self.secondary.state_properties.currentStateVector
            t_span          = np.array([self.time_vector[0], self.time_vector[-1]])
           
            def dynamics(t, state_vector):
                x, y, z = state_vector[0:3]
                r = np.linalg.norm([x, y, z])
                vx, vy, vz = state_vector[3:6]

                ax = -mu * x / r**3
                ay = -mu * y / r**3
                az = -mu * z / r**3

                return [vx, vy, vz, ax, ay, az]

            sol = solve_ivp(
                dynamics,
                t_span,
                state_vector,
                method="RK45",
                rtol=self.rel_tolerance,
                atol=self.abs_tolerance,
            )
            self.secondary.state_properties.stateHistory = sol.y.T
            return sol.t, sol.y

class CircularRestrictedThreeBodyPropagator(Propagator):
    def __init__(self):
        super().__init__()
        self.propagator_name        = "Circular Restricted Three-Body Propagator"
        self.propagator_source      = None
        self.propagator_description = "Propagates orbits using the circular restricted three-body problem solution."
        self.time_step              = 60.0  # seconds
        self.abs_tolerance          = 1e-9
        self.rel_tolerance          = 1e-9
        self.time_vector            = np.array([])
    @property
    def primary(self):
        return self.body_list[0]
    
    @property
    def secondary(self):
        return self.body_list[1]
    
    @property
    def tertiary(self):
        return self.body_list[2]

    def convertToNonDimRoationalFrame(self):
        self.NonDim_System = NonDimensionalSystem()
        self.NonDim_Primary = NonDimensionalBody()
        self.NonDim_Secondary = NonDimensionalBody()
        self.NonDim_Tertiary = NonDimensionalBody()

        if self.primary.physical_properties.mass is None: 
            raise ValueError("Unset Value Error")
        if self.secondary.physical_properties.mass is None: 
            raise ValueError("Unset Value Error")
        if self.primary.physical_properties.radius is None: 
            raise ValueError("Unset Value Error")
        if self.secondary.physical_properties.radius is None: 
            raise ValueError("Unset Value Error")
        if self.tertiary.state_properties.currentStateVector is None: 
            raise ValueError("Unset Value Error")

        self.NonDim_System._nd_m  = self.primary.physical_properties.mass + self.secondary.physical_properties.mass
        self.NonDim_System._nd_mu = self.secondary.physical_properties.mass / self.NonDim_System._nd_m
        self.NonDim_System._nd_l  = float(np.linalg.norm(self.secondary.state_properties.position))
        self.NonDim_System._nd_t  = (self.NonDim_System._nd_l**3 / (CommonParameter.G.parameter_value * self.NonDim_System._nd_m))**0.5

        self.NonDim_Primary._nd_m = self.primary.physical_properties.mass / self.NonDim_System._nd_m
        self.NonDim_Primary._nd_radius = self.primary.physical_properties.radius / self.NonDim_System._nd_l
        self.NonDim_Primary._nd_currentStateVector[0:3] = np.array([-self.NonDim_System._nd_mu,0,0])  # Assumption of the circular restricted three body problem, inplane
        self.NonDim_Primary._nd_currentStateVector[3:6] = np.array([0,0,0])        

        self.NonDim_Secondary._nd_m = self.secondary.physical_properties.mass / self.NonDim_System._nd_m
        self.NonDim_Secondary._nd_radius = self.secondary.physical_properties.radius / self.NonDim_System._nd_l
        self.NonDim_Secondary._nd_currentStateVector[0:3] = np.array([1-self.NonDim_System._nd_mu,0,0]) # Assumption of the circular restricted three body problem, inplane
        self.NonDim_Secondary._nd_currentStateVector[3:6] = np.array([0,0,0])

        self.NonDim_Tertiary._nd_currentStateVector[0:3] = self.tertiary.state_properties.currentStateVector[0:3]/self.NonDim_System._nd_l
        self.NonDim_Tertiary._nd_currentStateVector[3:6] = self.tertiary.state_properties.currentStateVector[3:6]*self.NonDim_System._nd_t / self.NonDim_System._nd_l
        self.NonDim_System._nd_timeVector = self.time_vector/self.NonDim_System._nd_t

        return self.NonDim_System
    
    def Convert_NonDimSys_to_DimSys(self):
        Position = self.NonDim_Tertiary._nd_stateHistory[:, 0:3] * self.NonDim_System._nd_l
        Velocity = self.NonDim_Tertiary._nd_stateHistory[:, 3:6] * self.NonDim_System._nd_t / self.NonDim_System._nd_l
        Time     = self.NonDim_Tertiary._nd_timeHistory  * self.NonDim_System._nd_t
        self.tertiary.state_properties.stateHistory = np.hstack((Position, Velocity))
        self.tertiary.state_properties.timeHistory = Time

    def cr3bp_rot_to_inertial(self, state_rot, t, omega=1.0, theta0=0.0):
        """
        Convert state from CR3BP rotating (synodic) frame to inertial frame.

        state_rot : array-like shape (6,) or (6,N)
            [x,y,z,vx,vy,vz] in rotating frame.
        t : float or array-like
            Time (same shape as columns in state_rot if array).
        omega : float
            Angular rate of rotating frame (rad/s). In normalized CR3BP units use omega=1.
        theta0 : float
            Rotation angle at t=0 (rad).

        Returns
        -------
        state_inert : ndarray same shape as state_rot
            State in inertial frame [x,y,z,vx,vy,vz].
        """
        state_rot = state_rot.T
        s = np.asarray(state_rot)
        single = (s.ndim == 1)
        if single:
            s = s.reshape(6, 1)

        t_arr = np.atleast_1d(t)
        
        if t_arr.size == 1 and s.shape[1] != 1:
            t_arr = np.full(s.shape[1], t_arr[0])
        elif t_arr.size != s.shape[1]:
            raise ValueError("time length must match number of state columns or be scalar")

        thetas = theta0 + omega * t_arr

        rs = s[0:3, :]
        vs = s[3:6, :]

        state_out = np.zeros_like(s)
        for i, theta in enumerate(thetas):
            c = np.cos(theta)
            si = np.sin(theta)
            R = np.array([[c, -si, 0.0],
                        [si,  c, 0.0],
                        [0.0, 0.0, 1.0]])
            r_i = R @ rs[:, i]
            v_i = R @ vs[:, i] + np.cross([0.0, 0.0, omega], r_i)
            state_out[0:3, i] = r_i
            state_out[3:6, i] = v_i
        state_out = state_out.T
        if single:
            return state_out[:, 0]
        return state_out


    def Propagate(self):
        self.convertToNonDimRoationalFrame()
        mu              = self.NonDim_System._nd_mu
        state_vector    = self.NonDim_Tertiary._nd_currentStateVector
        t_span          = np.array([self.NonDim_System._nd_timeVector[0], self.NonDim_System._nd_timeVector[-1]])
           
            
        def xdot(t, SV):
            x, y, z, dx, dy, dz = SV

            r1 = np.array([x + mu, y, z])
            r2 = np.array([x - 1 + mu, y, z])

            d1 = np.linalg.norm(r1)**3
            d2 = np.linalg.norm(r2)**3

            ddx =  2*dy + x - ( (1-mu)*(x+mu)/d1 ) - ( mu*(x-1+mu)/d2 )
            ddy = -2*dx + y - ( (1-mu)*y/d1 )     - ( mu*y/d2 )
            ddz = - ( (1-mu)*z/d1 )               - ( mu*z/d2 )
            
            return np.array([dx, dy, dz, ddx, ddy, ddz])

        sol = solve_ivp(xdot, [t_span[0], t_span[-1]], state_vector, method = 'RK45', rtol=1e-12, atol=1e-15)
        self.NonDim_Tertiary._nd_stateHistory = sol.y.T
        self.NonDim_Tertiary._nd_timeHistory = sol.t
        NonDim_Inertial = self.cr3bp_rot_to_inertial(self.NonDim_Tertiary._nd_stateHistory, self.NonDim_Tertiary._nd_timeHistory, omega=1.0, theta0=0.0)
        self.NonDim_Tertiary._nd_stateHistory = NonDim_Inertial

        self.Convert_NonDimSys_to_DimSys()
        return sol.t, sol.y
    
class NonDimensionalSystem:
    def __init__(self):
        self._nd_m      = 0.0  # Characteristic Mass
        self._nd_mu     = 0.0  # Characteristic Mass Ratio  
        self._nd_l      = 0.0  # Characteristic Length 
        self._nd_t      = 0.0  # Characteristic Time
        self._nd_timeVector = np.zeros(0)

class NonDimensionalBody:
    def __init__(self):
        self._nd_m                  : float             = 0.0
        self._nd_a                  : float             = 0.0
        self._nd_radius             : float             = 0.0
        self._nd_currentStateVector : np.ndarray       = np.zeros(6)
        self._nd_stateHistory       : np.ndarray       = np.zeros((0, 6))  # 2D: (timesteps, 6)
        self._nd_timeHistory        : np.ndarray       = np.zeros(0)       # 1D: (timesteps,)
