import math
from Calculations.dome_dimensions import dome_properties

def composite_density(fibre_density, resin_density, fibre_volume_fraction):
    # Volume-weighted average (rule of mixtures), NOT a simple 50/50 mean:
    # 72 % of the volume is fibre, 28 % is resin.
    return (fibre_volume_fraction * fibre_density
            + (1 - fibre_volume_fraction) * resin_density)

def tank_mass(liner_outer_radius, liner_thickness, overwrap_thickness,
              cylinder_length, polar_boss_opening, fibre_volume_fraction,
              al_density, fibre_density, resin_density):
    R   = liner_outer_radius      # liner outer radius = overwrap inner radius
    t_l = liner_thickness
    t_w = overwrap_thickness

    # --- Cylinder: volume of a hollow tube = pi * (r_outer^2 - r_inner^2) * length
    v_liner_cyl = math.pi * (R**2 - (R - t_l)**2) * cylinder_length
    v_wrap_cyl  = math.pi * ((R + t_w)**2 - R**2) * cylinder_length

    # --- Domes: shell volume = (volume inside the outer surface)
    #                         - (volume inside the inner surface).
    # dome_properties(R, t, r0) returns the volume inside a surface offset by t
    # from the liner's outer surface: t = 0 is the liner outer surface itself,
    # t > 0 offsets inwards (liner inner surface), t < 0 offsets outwards
    # (overwrap outer surface). Result is for ONE dome.
    v_outer_liner = dome_properties(R, 0.0, polar_boss_opening)["dome_volume"]
    v_inner_liner = dome_properties(R, t_l, polar_boss_opening)["dome_volume"]
    v_outer_wrap  = dome_properties(R, -t_w, polar_boss_opening)["dome_volume"]

    v_liner_dome = v_outer_liner - v_inner_liner
    v_wrap_dome  = v_outer_wrap - v_outer_liner

    v_liner = v_liner_cyl + 2 * v_liner_dome
    v_wrap  = v_wrap_cyl  + 2 * v_wrap_dome

    rho_c = composite_density(fibre_density, resin_density, fibre_volume_fraction)

    liner_mass    = v_liner * al_density
    overwrap_mass = v_wrap * rho_c

    return dict(
        liner_mass        = liner_mass,
        overwrap_mass     = overwrap_mass,
        total_mass        = liner_mass + overwrap_mass,
        composite_density = rho_c,
    )