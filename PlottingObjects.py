import matplotlib.pyplot as plt
import ColorSchemeObjects as Color_Scheme


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
    return TrajectoryPlot
