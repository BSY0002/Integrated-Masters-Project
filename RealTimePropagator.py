import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import ColorSchemeObjects
import StandardPlots
from matplotlib.widgets import TextBox
import CommandModule
import heapq

class RealTimePropagator:
    def __init__(self, bodyList, sim_start_time=0.0):
        self.bodyList = bodyList
        self.sim_time = sim_start_time

        self.speed = 1.0
        self.running = False
        self.stopped = False

        self.pq, self.uid = initialize_heap(bodyList)
        self.last_wall_time = None
        self.CommandModule = CommandModule.CommandModuleObject(bodyList, sim_start_time, self)



    # ======================================================
    # Simulation step
    # ======================================================
    def step(self):
        if not self.running or self.stopped:
            return

        now = time.perf_counter()
        dt_wall = now - self.last_wall_time
        self.last_wall_time = now

        dt_sim = self.speed * dt_wall
        self.sim_time += dt_sim

        self.pq, self.uid = propagate_until(
            self.bodyList,
            self.pq,
            self.uid,
            self.sim_time
        )

        self.CommandModule.process_commands()

    def RunRealTimeSimulation(self):
        fig, ax, artists, trail_buffers = self.initialize_scene(self.bodyList)

        self.CommandModule.set_speed(100.0)
        self.CommandModule.play()

        def on_timer():
            if self.stopped:
                return

            self.step()
            self.update_visual(
                bodies=self.bodyList,
                artists=artists,
                sim_time=self.sim_time,
                trail_buffers=trail_buffers
            )

            fig.figure.canvas.draw_idle()

        timer = fig.figure.canvas.new_timer(interval=16)  # ~60 Hz
        timer.add_callback(on_timer)
        timer.start()

        plt.show(block=True)

    # ======================================================
    # Visualization
    # ======================================================
    def update_visual(self, bodies, artists, sim_time, trail_buffers, max_trail=200):
        for body in bodies:
            name = body.name
            SP = body.StateProperties
            state = SP.orbit_state_at_time(sim_time)

            if state is None:
                continue

            x, y = state[0], state[1]
            buf = trail_buffers[name]
            buf["x"].append(x)
            buf["y"].append(y)

            if len(buf["x"]) > max_trail:
                buf["x"] = buf["x"][-max_trail:]
                buf["y"] = buf["y"][-max_trail:]

            artists[name]["trail"].set_data(buf["x"], buf["y"])
            artists[name]["marker"].set_offsets(np.array([[x, y]]))

    def initialize_scene(self, bodyList):
        plt.ion()
        fig = StandardPlots.FigureObject(
            ColorScheme=ColorSchemeObjects.VisualScheme_RetroMilitary
        )

        artists = {}
        trail_buffers = {}

        for body in bodyList:
            name = body.name
            VP = body.VisualProperties

            trail_buffers[name] = {"x": [], "y": []}

            trail, = fig.ax.plot([], [], color=VP.lineColor, linewidth=VP.lineWidth)
            marker = fig.ax.scatter(
                [0], [0],
                s=VP.size,
                marker=VP.icon,
                facecolor=VP.bodyColor,
                edgecolor=VP.edgeColor,
                linewidth=VP.lineWidth,
                zorder=3
            )

            if hasattr(body.PhysicalProperties, "radius"):
                fig.ax.add_patch(
                    Circle(
                        (0, 0),
                        body.PhysicalProperties.radius,
                        facecolor=VP.bodyColor,
                        edgecolor=VP.edgeColor,
                        alpha=0.8
                    )
                )

            artists[name] = {"trail": trail, "marker": marker}
        # -------------------------------
        # Command input box
        # -------------------------------
        axbox = fig.figure.add_axes([0.1, 0.01, 0.8, 0.05])
        textbox = TextBox(axbox, "CMD: ")
        textbox.on_submit(self.CommandModule.parse_command)

        self.textbox = textbox
        fig.ax.grid(True)
        plt.show(block=False)

        return fig, fig.ax, artists, trail_buffers

def initialize_heap(bodyList):
    pq = []
    uid = 0
    for body in bodyList:
        IP = body.IntegratorProperties.orbit
        if IP.integrator is None:
            continue

        SP = body.StateProperties
        next_time = SP.orbit_latest_time + IP.dt
        heapq.heappush(pq, (next_time, uid, body))
        uid += 1
    return pq, uid

def propagate_until(bodyList, pq, uid, t_target):

    while pq:

        next_time, _, body = heapq.heappop(pq)
        if next_time > t_target:
            heapq.heappush(pq, (next_time, uid, body))
            uid += 1
            break

        IP = body.IntegratorProperties.orbit
        SP = body.StateProperties

        t_body = SP.orbit_latest_time
        dt = next_time - t_body

        if SP.collided:
            new_state = SP.orbit_stateCurrent.copy()
            t_new = next_time
        else:
            integrator = IP.integrator
            dynamics = IP.dynamics
            state = SP.orbit_state_at_time(t_body)

            if IP.integrator.adaptive:
                dt_try = dt
                while True:
                    new_state, err, tol = integrator.step(
                        dynamics, state, t_body, dt_try,
                        IP.absTol, IP.relTol
                    )
                    if err <= tol:
                        break
                    dt_try = max(IP.dt_min, 0.5 * dt_try)

                t_new = t_body + dt_try
                if err < 0.1 * tol:
                    dt_try = min(IP.dt_max, 1.5 * dt_try)
                IP.dt = dt_try
            else:
                new_state = integrator.step(dynamics, state, t_body, dt)
                t_new = t_body + dt

        SP.set_orbitState(t_new, new_state)
        next_time = SP.orbit_latest_time + IP.dt
        # print(f"Body : {body.name} : Time : {next_time} : POS : {body.StateProperties.orbit_stateCurrent}")
        heapq.heappush(pq, (next_time, uid, body))
        uid += 1

    return pq, uid
