
class ColorScheme:
    def __init__(self):
        self.VisualSchemeDefault        = self.VisualScheme_Default()
        self.VisualSchemeRetroMilitary  = self.VisualScheme_RetroMilitary()

    class VisualScheme_Default:
        class Figure:
            # Plot Parameters
            backgroundColor = "#FFFFFF"
            gridColor = "#000000"
            axisColor = "#FFFFFF"
            textColor = "#000000"
            lineWidth = .25

        class Primary:
            # Primary Body Parameters
            bodyColor = "#1313C9"
            edgeColor = "#000000"
            lineColor = "#1313C9"
            textColor = "#1313C9"
            lineWidth = 1
            size = 500
            icon = '.'

        class Secondary:
            # Secomdary Body Parameters
            bodyColor = "#CC1100"
            edgeColor = "#000000"
            lineColor = "#CC1100"
            textColor = "#CC1100"
            lineWidth = 1
            size = 300
            icon = '.'

        class Tertiary:
            # Secomdary Body Parameters
            bodyColor = "#336234"
            edgeColor = "#000000"
            lineColor = "#336234"
            textColor = "#336234"
            lineWidth = 1
            size = 50
            icon = '>'
        
    class VisualScheme_RetroMilitary:
        class Figure:
            # Plot Parameters
            backgroundColor = "#000000"
            gridColor = "#FFCC00"
            axisColor = "#000000"
            textColor = "#FFCC00"
            lineWidth = .25

        class Primary:
            # Primary Body Parameters
            bodyColor = "#000000"
            edgeColor = "#CC1100"
            lineColor = "#CC1100"
            textColor = "#CC1100"
            lineWidth = 1
            size = 500
            icon = '.'

        class Secondary:
            # Secomdary Body Parameters
            bodyColor = "#000000"
            edgeColor = "#CC1100"
            lineColor = "#CC1100"
            textColor = "#CC1100"
            lineWidth = 1
            size = 300
            icon = '.'

        class Tertiary:
            # Secomdary Body Parameters
            bodyColor = "#000000"
            edgeColor = "#4aff00"
            lineColor = "#4aff00"
            textColor = "#4aff00"
            lineWidth = 1
            size = 50
            icon = '>'
      