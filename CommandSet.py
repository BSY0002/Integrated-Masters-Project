import time
from RealTimePropagator import initialize_heap
import numpy as np

# =======================================================
# Planetary Bodies
# =======================================================
class Commands_Simulation():
    def play(self, RealTimePropagator):
        if not RealTimePropagator.stopped:
            RealTimePropagator.running = True
            RealTimePropagator.last_wall_time = time.perf_counter()

    def pause(self, RealTimePropagator):
        RealTimePropagator.running = False

    def stop(self, RealTimePropagator):
        RealTimePropagator.running = False
        RealTimePropagator.stopped = True

    def set_speed(self, RealTimePropagator, speed):
        RealTimePropagator.speed = float(speed)

    def reset_propagation(self, bodyList):
        """
        Clear all future integration events and restart propagation
        from the current states.
        """
        self.pq, self.uid = initialize_heap(bodyList)



# =======================================================
# Spacecraft Commands
# =======================================================
class SpacecraftCommands():
    def impulsive_burn(self, rt, body, dv):
        SP = body.StateProperties
        t = rt.sim_time

        # --------------------
        # Physics
        # --------------------
        state = SP.orbit_state_at_time(t).copy()
        state[3:6] += np.array(dv)
        SP.set_orbitState(t, state)
        rt.reset_propagation()

    def Perform_Maneuver(self):
        pass
    def Perform_AttitudeChangeManeuver(self):
        pass
    def Perform_ReactionWheelDesaturation(self):
        pass
    def Perform_Communications(self):
        pass
    def Perform_Destruction(self):
        pass
    def Perform_Downlink(self):
        pass
    def Perform_Crosslink(self):
        pass
    def Perform_CommandCancel(self):
        pass
    def Perform_StationKeeping(self):
        pass
    def Perform_SafeMode(self):
        pass
    def Perform_StartUp(self):
        pass
    def Perform_BuiltInTest(self):
        pass