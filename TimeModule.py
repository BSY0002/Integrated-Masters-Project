class Time:
    def __init__(self):
        self.TimeFrame = 'UTC'
        self.startTime = 0
        self.endTime = 2551443/1000
        self.duration = self.endTime - self.startTime
        self.global_dt = 1
        self.visualization_dt = 1

    def compute_globaldt(self, bodyList):
        self.global_dt = min(
                            body.IntegratorProperties.dt
                            for body in bodyList
                            if body.IntegratorProperties.integrator is not None
                            )
        return self.global_dt