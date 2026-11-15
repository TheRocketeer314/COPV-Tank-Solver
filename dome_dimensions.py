import math
from scipy.integrate import quad

def dome_properties(liner_outer_radius, liner_thickness, 
                    polar_boss_opening, stop_factor=1.23):
    R  = liner_outer_radius              # outer radius at the junction
    r0 = polar_boss_opening
    r1 = stop_factor * r0              # geodesic -> spherical cap handoff

    K = math.sqrt(R**2 - r0**2) / R**3

    def psi(r):                        # step 2
        c = K * r**3 / math.sqrt(r**2 - r0**2)
        return math.acos(min(c, 1.0))

    # --- outer depth of the geodesic part (r = R - s^2 substitution) ---
    s_max = math.sqrt(R - r1)
    x_stop = quad(lambda s: 2*s / math.tan(psi(R - s**2)), 0, s_max)[0]

    p1  = psi(r1)
    x_c = x_stop - r1 * math.tan(p1)   # sphere centre
    Rs  = r1 / math.cos(p1)            # sphere radius

    # --- inner volume of the geodesic part ---
    def dV(s):
        r = R - s**2
        p = psi(r)
        g = 2 - r0**2 / (r**2 - r0**2)           # 2 - tan^2(alpha)
        r_in = r - liner_thickness * math.cos(p)
        return math.pi * r_in**2 * (r - liner_thickness*math.cos(p)*g) / (r*math.tan(p)) * 2*s
    V_geo = quad(dV, 0, s_max)[0]

    # --- inner spherical cap (closed form) ---
    Ri   = Rs - liner_thickness
    r_in1 = r1 - liner_thickness * math.cos(p1)
    w1 = math.sqrt(Ri**2 - r_in1**2)
    w0 = math.sqrt(Ri**2 - r0**2)
    V_cap = math.pi * ((Ri**2*w0 - w0**3/3) - (Ri**2*w1 - w1**3/3))

    return dict(dome_volume=V_geo + V_cap,
                dome_depth=x_c + w0,   # inner depth, junction to boss opening
                )