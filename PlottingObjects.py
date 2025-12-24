import matplotlib.pyplot as plt
import ColorSchemeObjects as Color_Scheme
from matplotlib.animation import FuncAnimation


# Types of Figures and Plots
class FigureObject:
    def __init__(self, ColorScheme = Color_Scheme.ColorScheme.VisualScheme_Default.Figure):        
        self.background_color   : str     = ColorScheme.backgroundColor
        self.grid_Color         : str     = ColorScheme.gridColor
        self.axis_Color         : str     = ColorScheme.axisColor
        self.text_Color         : str     = ColorScheme.textColor
        self.line_width         : float   = ColorScheme.lineWidth
        self.axis_equal         : bool    = False
        self.grid               : bool    = True
        self.title              : str     = "Default Title"
    
        # Create the Actual Figure
        self.figure, self.ax = plt.subplots()

        # Set the Color Scheme
        self.setColorScheme(ColorScheme)
        
        return


    def setColorScheme(self, ColorScheme):
        self.background_color    = ColorScheme.backgroundColor
        self.grid_Color          = ColorScheme.gridColor
        self.axis_Color          = ColorScheme.axisColor
        self.text_Color          = ColorScheme.textColor
        self.line_width          = ColorScheme.lineWidth
        
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
    BodyPlot = plt.scatter(Body.state_properties.position[0], 
                           Body.state_properties.position[1], 
                                label       = Body.name,
                                color       = Body.visual_properties.bodyColor, 
                                edgecolor   = Body.visual_properties.edgeColor,
                                s           = Body.visual_properties.size,
                                marker      = Body.visual_properties.icon,
                                linewidth   = Body.visual_properties.lineWidth,
                                alpha       = 1,
                                zorder      = 99,
                     )
    return BodyPlot

def Plot_Trajectory(Body):
    TrajectoryPlot = plt.plot(Body.state_properties.stateHistory[:, 0], 
                              Body.state_properties.stateHistory[:, 1],
                              label       = f"{Body.name} Trajectory",
                              color       = Body.visual_properties.lineColor,
                              linewidth   = Body.visual_properties.lineWidth,
                              alpha       = 1,
                              zorder      = 99,
    )
    
    InitialLocation = plt.scatter(  Body.state_properties.stateHistory[0, 0], 
                                    Body.state_properties.stateHistory[0, 1], 
                                    label       = Body.name,
                                    color       = Body.visual_properties.bodyColor, 
                                    edgecolor   = Body.visual_properties.edgeColor,
                                    s           = Body.visual_properties.size,
                                    marker      = Body.visual_properties.icon,
                                    linewidth   = Body.visual_properties.lineWidth,
                                    alpha       = 1,
                                    zorder      = 99,
    )
    FinalLocation = plt.scatter(    Body.state_properties.stateHistory[-1, 0], 
                                    Body.state_properties.stateHistory[-1, 1], 
                                    label       = Body.name,
                                    color       = Body.visual_properties.edgeColor, 
                                    edgecolor   = Body.visual_properties.edgeColor,
                                    s           = Body.visual_properties.size,
                                    marker      = Body.visual_properties.icon,
                                    linewidth   = Body.visual_properties.lineWidth,
                                    alpha       = 1,
                                    zorder      = 99,
    )               

    return TrajectoryPlot, InitialLocation, FinalLocation

# ...existing code...
def Animate_Trajectories(bodies, Figure_Object, duration_sec=10, interval_ms=50):
    """
    Animate one or more bodies. `bodies` can be a single body or a list of bodies.
    Each body must have state_properties.stateHistory as an (N,6) array (x,y,...) or (N,2) at minimum.
    """
    if not isinstance(bodies, (list, tuple)):
        bodies = [bodies]

    # resolve axis from Figure_Object
    if hasattr(Figure_Object, "ax"):
        ax = Figure_Object.ax
    elif hasattr(Figure_Object, "axes"):
        ax = Figure_Object.axes[0]
    elif hasattr(Figure_Object, "figure") and Figure_Object.figure.axes:
        ax = Figure_Object.figure.axes[0]
    else:
        import matplotlib.pyplot as plt
        ax = plt.gca()

    # Validate and compute lengths
    histories = []
    for b in bodies:
        hist = getattr(b.state_properties, "stateHistory", None)
        if hist is None or len(hist) == 0:
            raise ValueError(f"Body '{b.name}' has no stateHistory to animate")
        histories.append(hist)

    num_points = max(len(h) for h in histories)
    target_frames = max(1, (duration_sec * 1000) // max(1, interval_ms))
    frame_step = max(1, num_points // target_frames)
    num_frames = (num_points + frame_step - 1) // frame_step

    # create artists for each body
    lines = []
    scatters = []
    for b in bodies:
        line, = ax.plot([], [],
                        label=f"{b.name} Trajectory",
                        color=getattr(b.visual_properties, "bodyColor", "white"),
                        linewidth=getattr(b.visual_properties, "lineWidth", 1.0),
                        zorder=50)
        scatter = ax.scatter([], [],
                             label=b.name,
                             c=[getattr(b.visual_properties, "bodyColor", "white")],
                             edgecolor=getattr(b.visual_properties, "edgeColor", "k"),
                             s=getattr(b.visual_properties, "size", 20),
                             marker=getattr(b.visual_properties, "icon", "o"),
                             linewidths=getattr(b.visual_properties, "lineWidth", 1.0),
                             zorder=60)
        lines.append(line)
        scatters.append(scatter)

    def update(frame_idx):
        current_idx = frame_idx * frame_step
        artists = []
        for i, hist in enumerate(histories):
            idx = min(current_idx, len(hist) - 1)
            slice_ = hist[: idx + 1]
            # ensure numeric floats for matplotlib
            xs = [float(x) for x in slice_[:, 0]]
            ys = [float(y) for y in slice_[:, 1]]
            lines[i].set_data(xs, ys)
            scatters[i].set_offsets([[float(slice_[-1, 0]), float(slice_[-1, 1])]])
            artists.append(lines[i])
            artists.append(scatters[i])
        ax.relim()
        ax.autoscale_view()
        return tuple(artists)

    ani = FuncAnimation(
        Figure_Object.figure,
        update,
        frames=range(num_frames),
        interval=interval_ms,
        blit=True,
        repeat=True
    )
    return ani
# ...existing code...