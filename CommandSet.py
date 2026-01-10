# CommandSet.py
import numpy as np


# ======================================================
# Base Command Set (optional, for typing/structure)
# ======================================================
class BaseCommandSet:
    pass


# ======================================================
# Simulation Command Set
# ======================================================
class SimulationCommandSet(BaseCommandSet):
    def play(self, command, simulator):
        if not simulator.stopped:
            simulator.running = True

    def pause(self, command, simulator):
        simulator.running = False

    def set_speed(self, command, simulator):
        speed = float(command.arguments.get("speed", 1.0))
        simulator.speed = speed
# ======================================================
# Spacecraft Command Set
# ======================================================
class SpacecraftCommandSet(BaseCommandSet):
    """
    Operational spacecraft commands
    """

    def perform_maneuver(self, command, simulator, spacecraft):
        dv = np.array(command.arguments["dv"], dtype=float)
        t = simulator.sim_time

        SP = spacecraft.StateProperties
        state = SP.orbit_state_at_time(t).copy()
        state[3:6] += dv

        SP.set_orbitState(t, state)
        simulator.reset_propagation()

    def perform_attitude_change(self, command, simulator, spacecraft):
        pass

    def enter_safe_mode(self, command, simulator, spacecraft):
        pass

# ======================================================
# Planet Command Set
# ======================================================
class PlanetCommandSet(BaseCommandSet):
    pass
