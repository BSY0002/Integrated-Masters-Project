## Unit Tests
import ForceModels 
import IntegratorModels
import ObjectModels
import TimeModule 
import PropagatorModels

def TwoBodyPropagationTest(PrimaryBody = ObjectModels.Earth(), TimeElement = TimeModule.Time()):
# Create Test Space Vehicles
    UnitTestSpaceVehicle = ObjectModels.TestSpaceVehicle()
    UnitTestSpaceVehicle.name = "Unit Test Vehicle"

    # Define Forces
    pm = ForceModels.PointMassGravity(PrimaryBody)

    # Concatenate Forces
    Dynamics = IntegratorModels.Dynamics([pm])

    # Run RK4
    integrator_RK4 = IntegratorModels.RK4Integrator()
    UnitTestSpaceVehicle.StateProperties.stateHistory = PropagatorModels.Propagate(UnitTestSpaceVehicle.StateProperties.state, TimeElement, integrator_RK4, Dynamics)
    
    UnitTestSpaceVehicle.VisualProperties.bodyColor = "#000000"
    UnitTestSpaceVehicle.VisualProperties.edgeColor = "#CC1100"
    UnitTestSpaceVehicle.VisualProperties.lineColor = "#CC1100"
    UnitTestSpaceVehicle.VisualProperties.textColor = "#CC1100"
    UnitTestSpaceVehicle.VisualProperties.lineWidth = .25
    UnitTestSpaceVehicle.VisualProperties.size = 15
    UnitTestSpaceVehicle.VisualProperties.icon = '^'

    return UnitTestSpaceVehicle