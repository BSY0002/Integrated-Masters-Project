import numpy as np

class CircularEphemeris:
    def __init__(self, body, centralBody, epoch=0.0, plane="xy"):
        self.a = np.linalg.norm(body.StateProperties.stateCurrent[0:3])
        self.mu = centralBody.PhysicalProperties.mu
        self.n = np.sqrt(self.mu / self.a**3)
        self.epoch = epoch
        self.plane = plane

    def __call__(self, t):
        dt = t - self.epoch
        theta = self.n * dt

        c, s = np.cos(theta), np.sin(theta)
        vmag = self.n * self.a

        if self.plane == "xy":
            r = np.array([ self.a*c, self.a*s, 0.0 ])
            v = np.array([ -vmag*s, vmag*c, 0.0 ])
        else:
            r = np.array([ self.a*c, 0.0, self.a*s ])
            v = np.array([ -vmag*s, 0.0, vmag*c ])

        return np.hstack((r, v))

class KeplerianEphemeris:
    def __init__(self, mu, elements, epoch=0.0):
        self.mu = mu
        self.a, self.e, self.i, self.O, self.w, self.M0 = elements
        self.epoch = epoch
        self.n = np.sqrt(mu / self.a**3)

    def kepler_E(self, M):
        E = M
        for _ in range(8):
            E -= (E - self.e*np.sin(E) - M) / (1 - self.e*np.cos(E))
        return E

    def __call__(self, t):
        M = self.M0 + self.n*(t - self.epoch)
        E = self.kepler_E(M)

        r_p = self.a*(1 - self.e*np.cos(E))
        nu = 2*np.arctan2(
            np.sqrt(1+self.e)*np.sin(E/2),
            np.sqrt(1-self.e)*np.cos(E/2)
        )

        r = r_p * np.array([np.cos(nu), np.sin(nu), 0.0])
        v = np.sqrt(self.mu*self.a)/r_p * np.array([-np.sin(E), np.sqrt(1-self.e**2)*np.cos(E), 0])

        return np.hstack((r, v))


## 
class TabulatedEphemeris:
    def __init__(self, times, states):
        self.times = np.asarray(times)
        self.states = np.asarray(states)

    def __call__(self, t):
        if t <= self.times[0]:
            return self.states[0]
        if t >= self.times[-1]:
            return self.states[-1]

        i = np.searchsorted(self.times, t) - 1
        t0, t1 = self.times[i], self.times[i+1]
        s0, s1 = self.states[i], self.states[i+1]

        w = (t - t0) / (t1 - t0)
        return (1 - w)*s0 + w*s1
