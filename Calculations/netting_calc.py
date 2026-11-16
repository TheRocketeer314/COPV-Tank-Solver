def netting_calc(tank_radius, meop, safety_factor, 
                 fibre_allowable_stress, translation_efficiency, 
                 fibre_volume_fraction, al_yield_strength):
    # NOTE: tank_radius is now the OUTER radius of the overwrap
    tank_outer_radius = tank_radius #m

    max_design_pressure = meop * safety_factor #Pa
    fibre_design_stress = fibre_allowable_stress * translation_efficiency #Pa

    # Overwrap thickness = k * (overwrap inner radius), from the netting equations
    # (helical + hoop thickness = 1.5 * P * r / sigma, independent of wind angle)
    k = 1.5 * max_design_pressure / (fibre_design_stress * fibre_volume_fraction)

    # Liner thickness = c * (liner inner radius), axial thin-wall formula
    c = max_design_pressure / (2 * al_yield_strength)

    # Work inwards from the overwrap outer radius
    liner_outer_radius = tank_outer_radius / (1 + k) #m, = overwrap inner radius
    tank_inner_radius = liner_outer_radius / (1 + c) #m

    liner_thickness = liner_outer_radius - tank_inner_radius #m
    overwrap_thickness = tank_outer_radius - liner_outer_radius #m

    return dict(
        r_in    = tank_inner_radius,
        r_lo    = liner_outer_radius,
        t_liner = liner_thickness,
        t_wrap  = overwrap_thickness,
    )