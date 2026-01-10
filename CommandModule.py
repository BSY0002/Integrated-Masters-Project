## Command Module
import heapq
import numpy as np

class CommandModuleObject():
    def __init__(self, bodyList, sim_time, RealTimePropagator):
        self.bodyList = bodyList
        self.sim_time = sim_time
        self.command_queue = []
        self.RealTimePropagator = RealTimePropagator
    # def parse_command(self, cmd):
    #     tokens = cmd.strip().split()
    #     if not tokens:
    #         return

    #     sat = self.bodyList[1]  # LEO satellite

    #     if tokens[0] == "play":
    #         self.play()

    #     elif tokens[0] == "pause":
    #         self.pause()

    #     elif tokens[0] == "stop":
    #         self.stop()

    #     elif tokens[0] == "speed":
    #         self.set_speed(tokens[1])

    #     elif tokens[0] == "burn":
    #         delay = float(tokens[1])
    #         print(tokens)
    #         dv = [float(tokens[2]), float(tokens[3]), float(tokens[4])]
    #         self.schedule_command(
    #             delay,
    #             lambda: impulsive_burn(self, sat, dv)
    #         )

    def get_body_by_name(self, name):
        for body in self.bodyList:
            if body.name.lower() == name.lower():
                return body
        raise ValueError(f"Body '{name}' not found")

    def parse_command(self, cmd):
        tokens = cmd.strip().split()
        if not tokens : 
            return
        ObjectToken     = tokens[0]     # Token 0  = Name of Body, Satellite, Simulation, etc
        CommandToken    = tokens[1]     # Token 1  = Name of Command
        VariablesToken  = tokens[2:]    # Token 2: = Variables that are needed for command

        # Print Full Command Set
        print(f"Full CMD        : {cmd}")
        print(f"Object Token    : {ObjectToken}")
        print(f"Command Token   : {CommandToken}")
        print(f"Variables Token : {VariablesToken}")
        
        Object = self.get_body_by_name(ObjectToken)
        ObjectType = Object.__class__.__mro__

    # ======================================================
    # Command handling
    # ======================================================
    def schedule_command(self, delay, action):
        exec_time = self.sim_time + delay
        heapq.heappush(self.command_queue, (exec_time, action))

    def process_commands(self):
        while self.command_queue:
            exec_time, action = self.command_queue[0]
            if exec_time > self.sim_time:
                break
            heapq.heappop(self.command_queue)
            action()

