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
    BodyPlot = plt.scatter(Body.StateProperties.stateHistory[0, 0], 
                           Body.StateProperties.stateHistory[0, 1], 
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
    TrajectoryPlot = plt.plot(Body.StateProperties.stateHistory[:, 0], 
                              Body.StateProperties.stateHistory[:, 1],
                              label       = f"{Body.name} Trajectory",
                              color       = Body.VisualProperties.lineColor,
                              linewidth   = Body.VisualProperties.lineWidth,
                              alpha       = 1,
                              zorder      = 99,
    )

    return TrajectoryPlot

def Animate_Trajectories(bodies, Figure_Object):

    if not isinstance(bodies, (list, tuple)):
        bodies = [bodies]

    ax = Figure_Object.ax
    fig = Figure_Object.figure

    # -------------------------------------------------
    # GLOBAL ANIMATION TIME (decoupled from simulation)
    # -------------------------------------------------
    t_start = max(b.StateProperties.times[0] for b in bodies)
    t_end   = min(b.StateProperties.times[-1] for b in bodies)

    duration_sec, interval_ms, num_frames = compute_animation_timing(bodies)
    t_anim = np.linspace(t_start, t_end, num_frames)
    
    # -------------------------------------------------
    # Create artists
    # -------------------------------------------------
    lines = []
    markers = []

    for b in bodies:
        line, = ax.plot([], [],
                        linewidth=b.VisualProperties.lineWidth,
                        color=b.VisualProperties.lineColor)

        marker, = ax.plot([], [],
                          marker=b.VisualProperties.icon,
                          color=b.VisualProperties.lineColor,
                          markersize=0.75 * np.sqrt(b.VisualProperties.size),
                          linestyle='None')

        lines.append(line)
        markers.append(marker)

    # -------------------------------------------------
    # Trail buffers (bounded)
    # -------------------------------------------------
    MAX_TRAIL = 500
    trails = [{"x": [], "y": []} for _ in bodies]

    # -------------------------------------------------
    # Frame update
    # -------------------------------------------------
    def update(frame):
        t = t_anim[frame]
        artists = []

        for i, b in enumerate(bodies):
            state = b.StateProperties.state_at_time(t)
            x, y = state[0], state[1]

            trails[i]["x"].append(x)
            trails[i]["y"].append(y)

            if len(trails[i]["x"]) > MAX_TRAIL:
                trails[i]["x"] = trails[i]["x"][-MAX_TRAIL:]
                trails[i]["y"] = trails[i]["y"][-MAX_TRAIL:]

            lines[i].set_data(trails[i]["x"], trails[i]["y"])
            markers[i].set_data([x], [y])

            artists.extend([lines[i], markers[i]])

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
    t_start = max(b.StateProperties.times[0] for b in bodies)
    t_end   = min(b.StateProperties.times[-1] for b in bodies)

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
