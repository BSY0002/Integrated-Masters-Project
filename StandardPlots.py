import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Types of Figures and Plots
class FigureObject:
    def __init__(self, ColorScheme):        
        self.background_color   : str     = ColorScheme.Figure.backgroundColor
        self.grid_Color         : str     = ColorScheme.Figure.gridColor
        self.axis_Color         : str     = ColorScheme.Figure.axisColor
        self.text_Color         : str     = ColorScheme.Figure.textColor
        self.line_width         : float   = ColorScheme.Figure.lineWidth
        self.axis_equal         : bool    = True
        self.grid               : bool    = True
        self.title              : str     = "Default Title"
    
        # Create the Actual Figure
        self.figure, self.ax = plt.subplots()

        # Set the Color Scheme
        self.setColorScheme(ColorScheme)
        
        return


    def setColorScheme(self, ColorScheme):
        self.background_color    = ColorScheme.Figure.backgroundColor
        self.grid_Color          = ColorScheme.Figure.gridColor
        self.axis_Color          = ColorScheme.Figure.axisColor
        self.text_Color          = ColorScheme.Figure.textColor
        self.line_width          = ColorScheme.Figure.lineWidth
        
        self.ax.set_facecolor(self.background_color)
        self.ax.set_title(self.title, color=self.text_Color)
        self.ax.spines['bottom'].set_color(self.axis_Color)
        self.ax.spines['top'].set_color(self.axis_Color)
        self.ax.spines['left'].set_color(self.axis_Color)
        self.ax.spines['right'].set_color(self.axis_Color)
        self.ax.xaxis.label.set_color(self.text_Color)
        self.ax.yaxis.label.set_color(self.text_Color)
        self.ax.tick_params(axis='x', colors=self.text_Color)
        self.ax.tick_params(axis='y', colors=self.text_Color)   
        self.figure.patch.set_facecolor(self.background_color)

        # Grid Settings
        self.ax.minorticks_on()
        self.ax.grid(
                which       =   'major', 
                color       =   self.grid_Color, 
                linestyle   =   '-', 
                linewidth   =   self.line_width, 
                alpha       =   0.5)

        # Customize minor grid lines
        self.ax.grid(
                which       =   'minor', 
                color       =   self.grid_Color, 
                linestyle   =   '-', 
                linewidth   =   self.line_width / 2, 
                alpha       =   0.5)

        if self.axis_equal:
            self.ax.set_aspect('equal', adjustable='box')
            

def Plot_Body(Body):
    BodyPlot = plt.scatter(Body.StateProperties.orbit_stateHistory[0, 0], 
                           Body.StateProperties.orbit_stateHistory[0, 1], 
                                label       = Body.name,
                                color       = Body.VisualProperties.bodyColor, 
                                edgecolor   = Body.VisualProperties.edgeColor,
                                s           = Body.VisualProperties.size,
                                marker      = Body.VisualProperties.icon,
                                linewidth   = Body.VisualProperties.lineWidth,
                                alpha       = 1,
                                zorder      = 99,
                     )
    return BodyPlot

def Plot_Trajectory(Body):
    TrajectoryPlot = plt.plot(Body.StateProperties.orbit_stateHistory[:, 0], 
                              Body.StateProperties.orbit_stateHistory[:, 1],
                              label       = f"{Body.name} Trajectory",
                              color       = Body.VisualProperties.lineColor,
                              linewidth   = Body.VisualProperties.lineWidth,
                              alpha       = 1,
                              zorder      = 99,
    )

    return TrajectoryPlot

def Plot_Axes(Body):
    # Initial attitude
    att0 = Body.StateProperties.attitude_stateHistory[0]
    q0 = att0[0:4]

    # Initial position (use body orbit state if available)
    orbit0 = Body.StateProperties.orbit_stateHistory[0]
    x0, y0 = orbit0[0], orbit0[1]

    # Body → inertial rotation
    C0 = quat_to_dcm(q0)

    # Body axes in inertial frame
    x_b = C0 @ np.array([1.0, 0.0, 0.0])
    y_b = C0 @ np.array([0.0, 1.0, 0.0])
    z_b = C0 @ np.array([0.0, 0.0, 1.0])

    axis_scale = 3*1E6

    # X body axis (red)
    plt.plot(
        [x0, x0 + axis_scale * x_b[0]],
        [y0, y0 + axis_scale * x_b[1]],
        color='r', linewidth=2, label='Body X'
    )

    # Y body axis (green)
    plt.plot(
        [x0, x0 + axis_scale * y_b[0]],
        [y0, y0 + axis_scale * y_b[1]],
        color='g', linewidth=2, label='Body Y'
    )

    # Z body axis (blue, projected)
    plt.plot(
        [x0, x0 + axis_scale * z_b[0]],
        [y0, y0 + axis_scale * z_b[1]],
        color='b', linewidth=2, label='Body Z (proj)'
    )



def Animate_Trajectories(bodies, Figure_Object):

    if not isinstance(bodies, (list, tuple)):
        bodies = [bodies]

    ax = Figure_Object.ax
    fig = Figure_Object.figure

    # -------------------------------------------------
    # GLOBAL ANIMATION TIME (decoupled from simulation)
    # -------------------------------------------------
    t_start = max(b.StateProperties._orbit_times[0] for b in bodies)
    t_end   = min(b.StateProperties._orbit_times[-1] for b in bodies)

    duration_sec, interval_ms, num_frames = compute_animation_timing(bodies)
    t_anim = np.linspace(t_start, t_end, num_frames)
    
    # -------------------------------------------------
    # Create artists
    # -------------------------------------------------
    lines = []
    markers = []
    axes_artists = []
    axis_scale = 3*1E6
    
    for b in bodies:
            line, = ax.plot([], [],
                            linewidth=b.VisualProperties.lineWidth,
                            color=b.VisualProperties.lineColor)

            marker, = ax.plot([], [],
                                marker=b.VisualProperties.icon,
                                color=b.VisualProperties.lineColor,
                                markersize=0.75 * np.sqrt(b.VisualProperties.size),
                                linestyle='None')
           
           
            bx, = ax.plot([], [], color='r', linewidth=1)  # body x-axis
            by, = ax.plot([], [], color='g', linewidth=1)  # body y-axis
            bz, = ax.plot([], [], color='b', linewidth=1)  # body y-axis

            axes_artists.append((bx, by, bz))
            lines.append(line)
            markers.append(marker)

    # -------------------------------------------------
    # Trail buffers (bounded)
    # -------------------------------------------------
    MAX_TRAIL = 10
    trails = [{"x": [], "y": []} for _ in bodies]

    # -------------------------------------------------
    # Frame update
    # -------------------------------------------------
    def update(frame):
        t = t_anim[frame]
        artists = []

        # Scale relative to body orbit size
        for i, b in enumerate(bodies):
            # Position
            orbit_state = b.StateProperties.orbit_state_at_time(t)
            x, y = orbit_state[0], orbit_state[1]

            trails[i]["x"].append(x)
            trails[i]["y"].append(y)
            if len(trails[i]["x"]) > MAX_TRAIL:
                trails[i]["x"] = trails[i]["x"][-MAX_TRAIL:]
                trails[i]["y"] = trails[i]["y"][-MAX_TRAIL:]
            lines[i].set_data(trails[i]["x"], trails[i]["y"])
            markers[i].set_data([x], [y])
            artists.extend([lines[i], markers[i]])

            # Attitude axes
            att_state = b.StateProperties.attitude_state_at_time(t)
            q = att_state[0:4]
            C = quat_to_dcm(q)

            x_b = C @ np.array([1.0, 0.0, 0.0])
            y_b = C @ np.array([0.0, 1.0, 0.0])
            z_b = C @ np.array([0.0, 0.0, 1.0])

            bx, by, bz = axes_artists[i]
            bx.set_data([x, x + axis_scale * x_b[0]], [y, y + axis_scale * x_b[1]])
            by.set_data([x, x + axis_scale * y_b[0]], [y, y + axis_scale * y_b[1]])
            bz.set_data([x, x + axis_scale * z_b[0]], [y, y + axis_scale * z_b[1]])

            artists.extend([bx, by, bz])

        return artists

    ani = FuncAnimation(
        fig,
        update,
        frames=num_frames,
        interval=interval_ms,
        blit=False,
        repeat=True
    )

    return ani

def compute_animation_timing(bodies,
                             target_fps=60,
                             min_duration=6.0,
                             max_duration=20.0,
                             min_interval_ms=10,
                             max_interval_ms=50):
    """
    Automatically compute duration_sec and interval_ms for smooth animation.

    Returns:
        duration_sec, interval_ms, num_frames
    """

    # Determine common time span
    t_start = max(b.StateProperties._orbit_times[0] for b in bodies)
    t_end   = min(b.StateProperties._orbit_times[-1] for b in bodies)

    sim_span = max(1e-6, t_end - t_start)

    # Frame budget
    # More simulation time → longer animation, but capped
    duration_sec = np.clip(
        sim_span / (24 * 3600),  # 1 day of sim ≈ 1 sec of animation
        min_duration,
        max_duration
    )

    # FPS selection
    interval_ms = int(1000 / target_fps)
    interval_ms = int(np.clip(interval_ms, min_interval_ms, max_interval_ms))

    num_frames = int(duration_sec * 1000 / interval_ms)

    return duration_sec, interval_ms, num_frames



def quat_to_dcm(q):
    q0, q1, q2, q3 = q
    return np.array([
        [1 - 2*(q2*q2 + q3*q3), 2*(q1*q2 - q0*q3),     2*(q1*q3 + q0*q2)],
        [2*(q1*q2 + q0*q3),     1 - 2*(q1*q1 + q3*q3), 2*(q2*q3 - q0*q1)],
        [2*(q1*q3 - q0*q2),     2*(q2*q3 + q0*q1),     1 - 2*(q1*q1 + q2*q2)]
    ])


