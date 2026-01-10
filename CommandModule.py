# CommandModule.py
import heapq
from dataclasses import dataclass
import CommandSet
import RealTimePropagator

# ======================================================
# Command Object
# ======================================================
@dataclass
class Command:
    target_name: str
    command_name: str
    arguments: dict
    issue_time: float


# ======================================================
# Command Module
# ======================================================
class CommandModule:
    def __init__(self, simulator, bodyList):
        self.simulator = simulator
        self.bodyList = bodyList
        self._queue = []
    # --------------------------------------------------
    # Parsing
    # --------------------------------------------------
    def parse(self, text: str):
        tokens = text.strip().split()
        if not tokens:
            return None
        target = tokens[0]
        command = tokens[1]
        args = {}
        
        print(tokens)

        for token in tokens[2:]:
            k, v = token.split("=")
            if "," in v:
                args[k] = [float(x) for x in v.split(",")]
            else:
                args[k] = float(v)

        # Use propagator.sim_time if available, else 0
        issue_time = self.propagator.sim_time if self.propagator else 0.0

        return Command(
            target_name=target,
            command_name=command,
            arguments=args,
            issue_time=issue_time
        )
        
    # --------------------------------------------------
    # Execution
    # --------------------------------------------------
    def execute(self, command: Command):
        target = self.get_target(command.target_name)
        if target is None:
            print(f"[CMD] unknown target: {command.target_name}")
            return

        handler = getattr(target, "CommandProperties", None)
        if handler is None:
            print(f"[CMD] target has no CommandProperties: {target}")
            return

        cmdset = handler.command_set
        method = getattr(cmdset, command.command_name, None)
        if method is None:
            print(f"[CMD] unknown command on target: {command.command_name}")
            return

        # Dispatch with correct signature
        if isinstance(cmdset, CommandSet.SpacecraftCommandSet):
            # Use propagator if available (has sim_time/reset_propagation)
            sim_for_cmd = self.propagator if self.propagator is not None else self.simulator
            method(command, sim_for_cmd, target)   # (command, propagator/sim, spacecraft)
        else:
            method(command, self.simulator)        # (command, simulator)      # (command, simulator)

    # --------------------------------------------------
    # Both
    # -------------------------------------------------- 
    def parse_and_execute(self, text: str):
        """Parse command text and immediately execute it."""
        cmd = self.parse(text)
        if cmd:
            self.execute(cmd)

    # --------------------------------------------------
    # Routing
    # --------------------------------------------------
    def get_target(self, name):
        """Route command to the correct target object."""
        name_lower = name.lower()
        
        # Check if targeting the simulator itself
        if name_lower in ("simulator", "sim"):
            return self.simulator
        
        # Check bodies in bodyList
        for body in self.bodyList:
            if body.name.lower() == name_lower:
                return body
        
        return None
    # --------------------------------------------------
    # Scheduling
    # --------------------------------------------------
    def submit(self, command):
        heapq.heappush(self._queue, (command.issue_time, command))

    # --------------------------------------------------
    # Execution
    # --------------------------------------------------
    def process(self, sim_time):
        while self._queue:
            exec_time, cmd = self._queue[0]
            if exec_time > sim_time:
                break

            heapq.heappop(self._queue)
            target = self.get_target(cmd.target_name)

            target.CommandProperties.execute(
                command=cmd,
                simulator=self.simulator,
                owner=target
            )
