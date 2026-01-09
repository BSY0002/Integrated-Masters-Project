
class ParameterObject:
    def __init__(self,  parameter_name          : str,
                        parameter_value         : float,
                        parameter_units         : str,
                        parameter_description   : str,
                        parameter_variable      : str):
        
        self.parameter_name             = parameter_name
        self.parameter_value            = parameter_value
        self.parameter_units            = parameter_units
        self.parameter_description      = parameter_description
        self.parameter_variable         = parameter_variable

G = ParameterObject(
    parameter_name        = "Gravitational Constant",
    parameter_value       = 6.67430e-11,
    parameter_units       = "m^3 / (kg·s^2)",
    parameter_description = "Universal gravitational constant in m^3 / (kg·s^2)",
    parameter_variable    = "G"
)

