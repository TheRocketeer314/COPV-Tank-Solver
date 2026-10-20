import math
import ezdxf
import numpy as np
from scipy.integrate import solve_ivp   
import matplotlib.pyplot as plt
from Inputs import tank_radius, meop, safety_factor, polar_boss_opening, al_yield_strength, cylinder_length
import os
from Plotting import plot_dome_profile, plot_tank_profile
from dotenv import load_dotenv
from DXF_Export import load, fit, add_spline

load_dotenv()  # Load environment variables from .env file

DIRECTORY = os.getenv("DIRECTORY")  # Get the directory from environment variable
os.chdir(DIRECTORY)  # Change working directory to the specified path

thickness = (meop * safety_factor * tank_radius) / (al_yield_strength * 2) #m

#Dome contour calculations

r_stop_target = 1.23 * polar_boss_opening

def local_alpha(r):
    ratio = polar_boss_opening / r
    ratio = max(min(ratio, 1.0), -1.0)   # guard against float overshoot
    return math.asin(ratio)

def step_derivative(psi, r):
    alpha = local_alpha(r)
    rm = r/(math.cos(psi) * (2 - math.tan(alpha)**2))
    dr_dpsi = -rm * math.sin(psi)
    dx_dpsi = rm * math.cos(psi)
    return dr_dpsi, dx_dpsi

r = tank_radius + thickness
r_in = tank_radius
x = 0.0
x_in = 0.0
psi = 0.0
dpsi = 0.005          # small fixed step in psi [radians]
max_steps = 500_000    # safety cap so a bad input can't loop forever

r_history = [r]
x_history = [x]
r_in_history = [r_in]
x_in_history = [x_in]
steps_taken = 0
reached_stop = False

for steps_taken in range(1, max_steps + 1):
    dr_dpsi, dx_dpsi = step_derivative(psi, r)
    r += dr_dpsi * dpsi
    x += dx_dpsi * dpsi
    psi += dpsi

    r_in = r - math.cos(psi) * thickness
    x_in = x - math.sin(psi) * thickness

    r_history.append(r)
    x_history.append(x)
    r_in_history.append(r_in)
    x_in_history.append(x_in)

    if r <= r_stop_target:
        reached_stop = True
        break 

if not reached_stop:
    raise RuntimeError(
        "Inflection point (r = 1.22*r0) was never reached within "
        f"{max_steps} steps / psi up to {psi:.3f} rad. Winding angle may "
        "be too steep (>~55 deg) for a geodesic dome to make sense here, "
        "or dpsi needs to be smaller."
    )

r_dome = np.array(r_history)
x_dome = np.array(x_history)
r_in_dome = np.array(r_in_history)
x_in_dome = np.array(x_in_history)
r_stop = r_dome[-1]
x_stop = x_dome[-1]
psi_stop = psi

print(f"Reached stop after {steps_taken} steps, psi = {math.degrees(psi_stop):.2f} deg")
print(f"Handoff point: r_stop = {r_stop:.3f} mm, x_stop = {x_stop:.3f} mm")

# Spherical cap calculations

# Tangent direction at the handoff point, from the same derivative function
dr_dpsi, dx_dpsi = step_derivative(psi_stop, r_stop)

# Solve for the sphere's center (0, x_c) using: (P - C) . tangent = 0
x_c = x_stop + (r_stop * dr_dpsi) / dx_dpsi

# Sphere radius = distance from center to handoff point

# psi at the handoff point is already known: psi_stop

# x_c = x_s - r_s * tan(psi_s)
x_c = x_stop - r_stop * math.tan(psi_stop)

# R_s = r_s / cos(psi_s)
sphere_radius = r_stop / math.cos(psi_stop)
print(f"Sphere center x_c = {x_c:.3f} mm, radius = {sphere_radius:.3f} mm")

# x(r) = x_c + sqrt(R_s^2 - r^2)   (the + branch)
r_cap = np.linspace(r_stop, polar_boss_opening, 25)
x_cap = x_c + np.sqrt(sphere_radius**2 - r_cap**2)

inner_radius = sphere_radius - thickness
r_cap_in = np.linspace(r_in_history[-1], polar_boss_opening, 25)
x_cap_in = x_c + np.sqrt(inner_radius**2 - r_cap_in**2)

print(f"Boss point reached at x = {x_cap[-1]:.3f} mm "
      f"(this is the boss axial position - it's an OUTPUT, not an input)")

#Plot the dome and local wind angle

#Combine dome end cap

x_out  = np.concatenate([x_dome,     x_cap[1:]])
r_out  = np.concatenate([r_dome,     r_cap[1:]])
x_in = np.concatenate([x_in_dome, x_cap_in[1:]])
r_in = np.concatenate([r_in_dome, r_cap_in[1:]])

plot_dome_profile(x_in, r_in, x_out, r_out, x_stop, r_stop, x_cap, r_cap, x_cap_in, r_cap_in, r_dome, polar_boss_opening)

#Plot the full tank profile 

# Near-end dome at x = 0: mirror x, reverse so x ascends from boss to junction
x_out_A  = -x_out[::-1]
r_out_A  =  r_out[::-1]
x_in_A = -x_in[::-1]
r_in_A =  r_in[::-1]

# Far-end dome at x = L: just shift
x_out_B  = x_out  + cylinder_length
r_out_B  = r_out
x_in_B = x_in + cylinder_length
r_in_B = r_in

# Full inner and outer lines. The straight cylinder is the segment between
# the last point of A (x=0, r=R) and the first point of B (x=L, r=R),
# so no extra points are needed.
x_out_full  = np.concatenate([x_out_A,  x_out_B])
r_out_full  = np.concatenate([r_out_A,  r_out_B])
x_in_full = np.concatenate([x_in_A, x_in_B])
r_in_full = np.concatenate([r_in_A, r_in_B])

plot_tank_profile(x_in_full, r_in_full, x_out_full, r_out_full, cylinder_length, tank_radius, thickness)

# EXPORT FOR CAD - one CSV per surface (x, r)

np.savetxt('dome_inner.csv', np.column_stack((x_in, r_in)),
           delimiter=',', header='x_mm,r_mm', comments='')
np.savetxt('dome_outer.csv', np.column_stack((x_out, r_out)),
           delimiter=',', header='x_mm,r_mm', comments='')
print("Exported dome_inner.csv and dome_outer.csv")

#Create DXF file with splines for the dome and cap

outer = fit(load("dome_outer.csv"))
inner = fit(load("dome_inner.csv"))

doc = ezdxf.new("R2010")
doc.units = ezdxf.units.MM
msp = doc.modelspace()

o_start, o_end = add_spline(msp, outer)
i_start, i_end = add_spline(msp, inner)

# close the profile: junction side and boss-opening side
msp.add_line(o_start, i_start)
msp.add_line(o_end, i_end)

doc.saveas("dome_profile.dxf")
print("saved dome_profile.dxf")