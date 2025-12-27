def Propagate(bodyList, TimeElement):
    for time in TimeElement.timeVector:
        for body in bodyList:

            integrator = body.IntegratorProperties.integrator
            dynamics   = body.IntegratorProperties.dynamics

            # Skip fixed bodies
            if integrator is None or dynamics is None:
                continue

            new_state = integrator.step(
                deriv_func=dynamics,
                state=body.StateProperties.stateCurrent,
                time=time,
                dt=TimeElement.timeStep
            )

            body.StateProperties.stateCurrent = new_state

    return bodyList
