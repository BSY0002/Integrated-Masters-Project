import heapq
import numpy as np
import ObjectModels
import IntegratorModels

def Propagate(bodyList, TimeElement):

    t_start = TimeElement.startTime
    t_end   = TimeElement.endTime

    # --------------------------------------------------
    # Initialize all bodies at t_start
    # --------------------------------------------------
    for body in bodyList:
        SP = body.StateProperties

        if SP.latest_time is None:
            SP.set_state(t_start, SP._stateCurrent)

        # Ensure collision flag exists
        if not hasattr(SP, "collided"):
            SP.collided = False

    # --------------------------------------------------
    # Priority queue: (next_time, uid, body)
    # --------------------------------------------------
    pq = []
    uid = 0

    for body in bodyList:
        IP = body.IntegratorProperties

        if IP.integrator is None:
            continue  # ephemeris / fixed body

        next_time = body.StateProperties.latest_time + IP.dt
        heapq.heappush(pq, (next_time, uid, body))
        uid += 1

    # --------------------------------------------------
    # Event-driven propagation loop
    # --------------------------------------------------
    while pq:

        next_time, _, body = heapq.heappop(pq)

        if next_time > t_end:
            break

        IP = body.IntegratorProperties
        SP = body.StateProperties

        t_body = SP.latest_time
        dt     = next_time - t_body

        # --------------------------------------------------
        # Frozen body after collision
        # --------------------------------------------------
        if SP.collided:
            new_state = SP.stateCurrent.copy()
            t_new = next_time

        else:
            integrator = IP.integrator
            dynamics   = IP.dynamics

            state = SP.state_at_time(t_body)

            # ----------------------------------------------
            # Adaptive RK4
            # ----------------------------------------------
            if isinstance(integrator, IntegratorModels.AdaptiveRK4Integrator):

                dt_try = dt

                while True:
                    new_state, err, tol = integrator.step(
                        deriv_func=dynamics,
                        state=state,
                        time=t_body,
                        dt=dt_try,
                        absTol=IP.absTol,
                        relTol=IP.relTol
                    )

                    if err <= tol:
                        break

                    dt_try = max(IP.dt_min, 0.5 * dt_try)

                t_new = t_body + dt_try

                if err < 0.1 * tol:
                    dt_try = min(IP.dt_max, 1.5 * dt_try)

                IP.dt = dt_try

            # ----------------------------------------------
            # Fixed-step integrator
            # ----------------------------------------------
            else:
                new_state = integrator.step(
                    deriv_func=dynamics,
                    state=state,
                    time=t_body,
                    dt=dt
                )
                t_new = t_body + dt

        # --------------------------------------------------
        # Collision detection
        # --------------------------------------------------
        if not SP.collided:
            for other in bodyList:

                if other is body:
                    continue

                if isinstance(body, ObjectModels.Planet):
                    continue

                if (
                    isinstance(body, ObjectModels.SpaceVehicle)
                    and isinstance(other, ObjectModels.SpaceVehicle)
                ):
                    continue

                other_state = other.StateProperties.state_at_time(t_new)
                r_rel = new_state[0:3] - other_state[0:3]

                if np.linalg.norm(r_rel) <= other.PhysicalProperties.radius:
                    SP.collided = True
                    print(f"Collision: {body.name} with {other.name}")
                    break

        # --------------------------------------------------
        # Commit state (always)
        # --------------------------------------------------
        SP.set_state(t_new, new_state)
        print(body.name + " : " + str(next_time) + " / " + str(t_end))
        # --------------------------------------------------
        # Schedule next event
        # --------------------------------------------------
        next_time = SP.latest_time + IP.dt
        heapq.heappush(pq, (next_time, uid, body))
        uid += 1

    return bodyList
