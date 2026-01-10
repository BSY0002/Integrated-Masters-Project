import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import ColorSchemeObjects
import StandardPlots
from matplotlib.widgets import TextBox
import CommandModule
import heapq
import ObjectModels

class RealTimePropagatorObject:
    def __init__(self, bodyList, sim_start_time=0.0):
        self.bodyList = bodyList
        self.sim_time = sim_start_time

        self.speed = 1.0
        self.running = False
        self.stopped = False

        self.pq, self.uid = initialize_heap(bodyList)

        self.last_wall_time = None
        self.wall_start_time = None

        self.simulation = ObjectModels.SimulationObject("simulator")
        self.CommandModule = CommandModule.CommandModule(self.bodyList, self.simulation)

    def reset_propagation(self):
        """Rebuild propagation queue after state changes (e.g., maneuvers)."""
        self.pq, self.uid = initialize_heap(self.bodyList)


    # ======================================================
    # Simulation step
    # ======================================================
    def step(self):
        # read authoritative flags from the SimulationObject
        self.running = bool(getattr(self.simulation, "running", self.running))
        self.stopped = bool(getattr(self.simulation, "stopped", self.stopped))
        self.speed = float(getattr(self.simulation, "speed", self.speed))

        if not self.running or self.stopped:
            self.last_wall_time = None
            return
        
        now = time.perf_counter()
        if self.last_wall_time is None:
            self.last_wall_time = now
            return

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

        self.CommandModule.process(self.sim_time)

    def RunRealTimeSimulation(self):
        fig, ax, artists, trail_buffers = self.initialize_scene(self.bodyList)
        
        # ensure simulation is running and initialize wall-clock reference
        self.simulation.running = True
        self.simulation.stopped = False
        self.running = True
        self.stopped = False

        # initialize wall clock (elapsed wall time reference)
        self.last_wall_time = time.perf_counter()
        self.wall_start_time = self.last_wall_time

        # Create and execute commands
        speed_cmd = CommandModule.Command(
            target_name="simulator",
            command_name="set_speed",
            arguments={"speed": 100.0},
            issue_time=self.sim_time
        )
        self.simulation.CommandProperties.execute(
            command=speed_cmd,
            simulator=self.simulation,
            owner=self.simulation
        )

        play_cmd = CommandModule.Command(
            target_name="simulator",
            command_name="play",
            arguments={},
            issue_time=self.sim_time
        )
        self.simulation.CommandProperties.execute(
            command=play_cmd,
            simulator=self.simulation,
            owner=self.simulation
        )

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
        
        # sync runtime speed with simulation object (commands update SimulationObject.speed)
        if hasattr(self.simulation, "speed"):
            self.speed = float(self.simulation.speed)

        # update overlay text
        sim_text = artists.get("sim_time_text")
        speed_text = artists.get("speed_text")
        wall_text = artists.get("wall_time_text")

        if sim_text is not None:
            sim_text.set_text(f"Sim t: {sim_time:.2f} s")

        if speed_text is not None:
            speed_text.set_text(f"Speed: {self.speed:.1f}x")

        if wall_text is not None:
            if self.wall_start_time is not None:
                wall_elapsed = time.perf_counter() - self.wall_start_time
                wall_text.set_text(f"Wall: {wall_elapsed:.2f} s")
            else:
                wall_text.set_text("Wall: --")

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
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
        """
        Build and return the plotting scene.

        Returns:
            fig_obj: StandardPlots.FigureObject
            ax: matplotlib Axes (fig_obj.ax)
            artists: dict mapping names to artists and overlay text
            trail_buffers: dict mapping body name -> {"x":[], "y":[]}
        """
        plt.ion()
        fig = StandardPlots.FigureObject(
            ColorScheme=ColorSchemeObjects.VisualScheme_RetroMilitary
        )
        ax = fig.ax

        # Overlay text in upper-left
        sim_text = ax.text(
            0.02, 0.98, "Sim t: 0.00 s",
            transform=ax.transAxes, va="top", ha="left",
            color="white", fontsize=10, bbox=dict(facecolor="black", alpha=0.5, pad=2)
        )
        speed_text = ax.text(
            0.02, 0.94, "Speed: 1.0x",
            transform=ax.transAxes, va="top", ha="left",
            color="white", fontsize=10, bbox=dict(facecolor="black", alpha=0.5, pad=2)
        )
        wall_text = ax.text(
            0.02, 0.90, "Wall: 0.00 s",
            transform=ax.transAxes, va="top", ha="left",
            color="white", fontsize=10, bbox=dict(facecolor="black", alpha=0.5, pad=2)
        )

        artists = {
            "sim_time_text": sim_text,
            "speed_text": speed_text,
            "wall_time_text": wall_text,
        }

        trail_buffers = {}

        # Create per-body trail and marker artists
        for body in bodyList:
            name = body.name
            VP = body.VisualProperties

            # Ensure visual properties exist and provide sane defaults
            line_color = getattr(VP, "lineColor", "white")
            line_width = getattr(VP, "lineWidth", 1.0)
            size = getattr(VP, "size", 20)
            icon = getattr(VP, "icon", "o")
            body_color = getattr(VP, "bodyColor", "gray")
            edge_color = getattr(VP, "edgeColor", "white")

            trail_buffers[name] = {"x": [], "y": []}

            trail, = ax.plot([], [], color=line_color, linewidth=line_width, zorder=2)
            marker = ax.scatter(
                [0], [0],
                s=size,
                marker=icon,
                facecolor=body_color,
                edgecolor=edge_color,
                linewidth=line_width,
                zorder=3
            )

            # Optionally draw physical body circle if radius present and > 0
            radius = getattr(body.PhysicalProperties, "radius", None)
            if radius:
                ax.add_patch(
                    Circle(
                        (0, 0),
                        radius,
                        facecolor=body_color,
                        edgecolor=edge_color,
                        alpha=0.8,
                        zorder=1
                    )
                )

            artists[name] = {"trail": trail, "marker": marker}

        # -------------------------------
        # Command input box
        # -------------------------------
        axbox = fig.figure.add_axes([0.1, 0.01, 0.8, 0.05])
        textbox = TextBox(axbox, "CMD: ")
        # parse expects a single text argument; keep behavior consistent
        textbox.on_submit(self.CommandModule.parse_and_execute)
        self.textbox = textbox

        # Final scene tweaks
        ax.grid(True)
        plt.show(block=False)

        return fig, ax, artists, trail_buffers
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
