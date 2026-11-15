from dome_dimensions import dome_properties
from netting_calc import netting_calc
from tank_calculations import cyl_volume, cyl_length, tank_length

def size_tank(volume, radius, meop, safety_factor, boss_opening, al_yield_strength, fibre_allowable_stress, translation_efficiency, fibre_volume_fraction):
    netting_calculation = netting_calc(radius, meop, safety_factor, fibre_allowable_stress, translation_efficiency, fibre_volume_fraction, al_yield_strength)
    tank_properties = dome_properties(radius, meop, safety_factor, boss_opening, al_yield_strength)

    dome_volume = tank_properties["dome_volume"]
    dome_depth = tank_properties["dome_depth"]

    cylinder_volume = cyl_volume(volume, dome_volume)
    cylinder_length = cyl_length(cylinder_volume, radius)

    total_tank_length = tank_length(cylinder_length, dome_depth)

    nitrous_liner_thickness = netting_calculation["t_liner"]

    #Find thickness and outer radius of the tank

    nitrous_overwrap_thickness = netting_calculation["t_wrap"]
    total_thickness = nitrous_liner_thickness + nitrous_overwrap_thickness

    return dict(
        tank_length = total_tank_length,
        total_thickness = total_thickness,
        cylinder_length = cylinder_length,
    )