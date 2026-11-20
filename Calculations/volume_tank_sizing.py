from Calculations.dome_dimensions import dome_properties
from Calculations.netting_calc import netting_calc
from Calculations.basic_dimension_calc import cyl_volume, cyl_length, tank_length

def size_tank(volume, radius, meop, safety_factor, boss_opening, al_yield_strength, 
              fibre_allowable_stress, translation_efficiency, fibre_volume_fraction, t_liner_min,
              liner_elastic_modulus, fibre_elastic_modulus):
    
    netting_calculation = netting_calc(radius, meop, safety_factor, fibre_allowable_stress, 
                                       translation_efficiency, fibre_volume_fraction, al_yield_strength,
                                       boss_opening, t_liner_min, liner_elastic_modulus, fibre_elastic_modulus)

    inner_radius = netting_calculation["r_in"]

    liner_thickness = netting_calculation["t_liner"]

    liner_outer_radius = netting_calculation["r_lo"]

    tank_properties = dome_properties(liner_outer_radius, liner_thickness, boss_opening)

    dome_volume = tank_properties["dome_volume"]
    dome_depth = tank_properties["dome_depth"]

    cylinder_volume = cyl_volume(volume, dome_volume)

    if cylinder_volume <= 0:
        raise ValueError("Tank volume is smaller than the two domes combined")
    
    cylinder_length = cyl_length(cylinder_volume, netting_calculation["r_in"])

    total_tank_length = tank_length(cylinder_length, dome_depth)

    #Find thickness and outer radius of the tank

    overwrap_thickness = netting_calculation["t_wrap"]
    total_thickness = liner_thickness + overwrap_thickness

    return dict(
        tank_length = total_tank_length,
        total_thickness = total_thickness,
        cylinder_length = cylinder_length,
        overwrap_thickness = overwrap_thickness,
        liner_thickness = liner_thickness,
        tank_outer_radius = radius,
        tank_inner_radius = inner_radius,
        liner_outer_radius = liner_outer_radius
    )