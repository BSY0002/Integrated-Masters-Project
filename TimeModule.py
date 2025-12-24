import numpy as np

class Time:
    def __init__(self):
        self.TimeFrame = 'UTC'
        self.startTime = 0
        self.endTime = 1000
        self.currentTime = 0
        self.timeStep = 1
        self.absoluteTolerance = 0.001
        self.relativeTolerance = 0.01
        self.duration = self.endTime - self.startTime
        self.timeVector = np.arange(self.startTime, self.endTime + self.timeStep, self.timeStep)