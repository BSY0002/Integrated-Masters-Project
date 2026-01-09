import heapq
import numpy as np
import ObjectModels
import IntegratorModels


def Propagate(bodyList, TimeElement):

    t_start = TimeElement.startTime
    t_end   = TimeElement.endTime

    # ==================================================
    # Initialization
    # ==================================================
    for body in bodyList:
        SP = body.StateProperties

        if SP.orbit_latest_time is None:
            SP.set_orbitState(t_start, SP.orbit_stateCurrent)

        if SP.attitude_latest_time is None:
            SP.set_attitudeState(t_start, SP.attitude_stateCurrent)

        if not hasattr(SP, "collided"):
            SP.collided = False

    # ==================================================
    # Priority queue: (next_sync_time, uid, body)
    # ==================================================
    pq  = []
    uid = 0

    for body in bodyList:
        IP = body.IntegratorProperties

        if not IP.orbit.is_propagated and not IP.attitude.is_propagated:
            continue

        t0 = body_sync_time(body.StateProperties)
        heapq.heappush(pq, (t0 + IP.sync_dt, uid, body))
        uid += 1

    # ==================================================
    # Event-driven propagation loop
    # ==================================================
    while pq:

        t_target, _, body = heapq.heappop(pq)

        if t_target > t_end:
            break

        SP = body.StateProperties
        IP = body.IntegratorProperties

        # ==================================================
        # ORBIT PROPAGATION
        # ==================================================
        if IP.orbit.is_propagated and not SP.collided:

            IPo = IP.orbit
            t   = SP.orbit_latest_time
            x   = SP.orbit_stateCurrent.copy()

            while t < t_target:

                dt = min(IPo.dt, t_target - t)

                if isinstance(IPo.integrator, IntegratorModels.AdaptiveRK45Integrator):

                    dt_try = dt
                    while True:
                        x_new, err, tol = IPo.integrator.step(
                            IPo.dynamics, x, t, dt_try,
                            IPo.absTol, IPo.relTol
                        )

                        if err <= tol:
                            break

                        dt_try = max(IPo.dt_min, 0.5 * dt_try)

                    x = x_new
                    t += dt_try

                    # Adapt step
                    if err > 0.0:
                        fac = 0.9 * (tol / err) ** 0.25
                        IPo.dt = np.clip(fac * dt_try, IPo.dt_min, IPo.dt_max)
                    else:
                        IPo.dt = min(IPo.dt_max, 2.0 * dt_try)

                else:
                    x = IPo.integrator.step(IPo.dynamics, x, t, dt)
                    t += dt

            SP.set_orbitState(t_target, x)

        # ==================================================
        # ATTITUDE PROPAGATION
        # ==================================================
        if IP.attitude.is_propagated and not SP.collided:

            IPa = IP.attitude
            t   = SP.attitude_latest_time
            q   = SP.attitude_stateCurrent.copy()

            while t < t_target:
                
                dt = min(IPa.dt, t_target - t)
                if isinstance(IPa.integrator, IntegratorModels.AdaptiveRK45Integrator):

                    dt_try = dt
                    while True:
                        q_new, err, tol = IPa.integrator.step(
                            IPa.dynamics, q, t, dt_try,
                            IPa.absTol, IPa.relTol
                        )

                        if err <= tol:
                            break

                        dt_try = max(IPa.dt_min, 0.5 * dt_try)

                    q = renormalize_quaternion_inplace(q_new)  # <-- normalize here
                    t += dt_try

                    if err > 0.0:
                        fac = 0.9 * (tol / err) ** 0.25
                        IPa.dt = np.clip(fac * dt_try, IPa.dt_min, IPa.dt_max)
                    else:
                        IPa.dt = min(IPa.dt_max, 2.0 * dt_try)

                else:
                    q = IPa.integrator.step(IPa.dynamics, q, t, dt)
                    q = renormalize_quaternion_inplace(q)  # <-- normalize here
                    t += dt

            SP.set_attitudeState(t_target, q)

        # ==================================================
        # COLLISION CHECK (SYNCHRONIZED)
        # ==================================================
        if not SP.collided and IP.orbit.is_propagated:

            r_body = SP.orbit_state_at_time(t_target)[0:3]

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

                r_other = other.StateProperties.orbit_state_at_time(t_target)[0:3]

                if np.linalg.norm(r_body - r_other) <= other.PhysicalProperties.radius:
                    SP.collided = True
                    print(f"Collision: {body.name} with {other.name}")
                    break

        # ==================================================
        # Schedule next synchronization
        # ==================================================
        next_time = t_target + IP.sync_dt
        heapq.heappush(pq, (next_time, uid, body))
        uid += 1

        print(f"{body.name} : {100.0 * t_target / t_end:.2f}%")

    return bodyList


def body_sync_time(SP):
    return min(SP.orbit_latest_time, SP.attitude_latest_time)

# numpy in-place variant
def renormalize_quaternion_inplace(q, tol=1e-12):
    # a is a length-4 numpy array [w,x,y,z]
    import numpy as np
    norm2 = float((q * q).sum())
    if abs(norm2 - 1.0) < tol:
        return q
    inv = 1.0 / np.sqrt(norm2)
    inv = inv * (1.5 - 0.5 * norm2 * inv * inv)
    q *= inv
    return q