import warnings

def netting_calc(tank_radius, meop, safety_factor,
                 fibre_allowable_stress, translation_efficiency,
                 fibre_volume_fraction, al_yield_strength,
                 polar_boss_opening=None, 
                 t_liner_min=3.0e-3,  
                 E_liner=69e9,         
                 E_fibre=230e9,         
                 hoop_share=None):    
    # NOTE: tank_radius is the OUTER radius of the overwrap
    tank_outer_radius = tank_radius #m

    max_design_pressure = meop * safety_factor #Pa
    fibre_design_stress = fibre_allowable_stress * translation_efficiency #Pa

    # --- Overwrap: carries ALL the load (hoop + axial) at design pressure ---
    # thickness = k * (overwrap inner radius), from the netting equations
    k = 1.5 * max_design_pressure / (fibre_design_stress * fibre_volume_fraction)

    liner_outer_radius = tank_outer_radius / (1 + k) #m, = overwrap inner radius
    overwrap_thickness = tank_outer_radius - liner_outer_radius #m

    # --- Liner: set by manufacturing, NOT by load ---
    # Old method (liner carries the whole axial load alone), kept only as an
    # upper bound / for comparison. It is not used for the design any more.
    c = max_design_pressure / (2 * al_yield_strength)
    t_liner_axial = liner_outer_radius - liner_outer_radius / (1 + c)

    liner_thickness = t_liner_min #m
    tank_inner_radius = liner_outer_radius - liner_thickness #m

    # --- Strain-compatibility check at MEOP (not at design pressure) ---
    # Liner and fibre stretch by the same amount; each carries
    # (stiffness x thickness x strain) of the load P*r.
    # Fraction of the overwrap fibre that works in the hoop direction.
    # Netting: hoop fibre ~ P*r*(1 - 0.5*tan^2(a)) / sigma, total fibre ~ 1.5*P*r / sigma,
    # so hoop_share = (1 - 0.5*tan^2(a)) / 1.5, with sin(a) = r_boss / r_winding.
    if hoop_share is None:
        if polar_boss_opening is not None:
            sin_a = polar_boss_opening / liner_outer_radius
            tan_sq = sin_a**2 / (1 - sin_a**2)
            hoop_share = (1 - 0.5 * tan_sq) / 1.5
        else:
            hoop_share = 2 / 3   # fallback when no boss opening is given

    t_hoop_fibre = hoop_share * fibre_volume_fraction * overwrap_thickness
    liner_strain = (meop * tank_inner_radius) / (
        E_liner * liner_thickness + E_fibre * t_hoop_fibre
    )
    liner_stress = E_liner * liner_strain #Pa

    if liner_stress > al_yield_strength:
        warnings.warn(
            f"Liner stress at MEOP ({liner_stress/1e6:.0f} MPa) exceeds yield "
            f"({al_yield_strength/1e6:.0f} MPa): liner will yield every cycle."
        )
    if liner_thickness > t_liner_axial:
        warnings.warn(
            "t_liner_min is thicker than the old axial-load thickness; "
            "the liner is heavier than it needs to be."
        )

    return dict(
        r_in    = tank_inner_radius,
        r_lo    = liner_outer_radius,
        t_liner = liner_thickness,
        t_wrap  = overwrap_thickness,
        t_liner_axial = t_liner_axial,
        liner_strain  = liner_strain,
        liner_stress  = liner_stress,
        hoop_share    = hoop_share,
    )