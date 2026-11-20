
from Calculations.coolprop_functions import density_TP
from Calculations.volume_tank_sizing import size_tank
from Calculations.converters import temp_C_to_K

def nitrous_tank_sizing(nitrous_radius, nitrous_mass, nitrous_meop, 
                        nitrous_ullage_fraction, ambient_temp, nitrous_safety_factor, 
                        nitrous_boss_opening, al_yield_strength,fibre_allowable_stress,
                        translation_efficiency, fibre_volume_fraction, nitrous_min_liner_thickness,
                        liner_elastic_modulus, fibre_elastic_modulus):
    
    ullage = nitrous_ullage_fraction

    # Calculate the tank length

    ambient_temp_K = temp_C_to_K(ambient_temp)
    rho = density_TP(ambient_temp_K, nitrous_meop, "NITROUSOXIDE")  # kg/m^3
    volume = (nitrous_mass / rho) / (1 - ullage)

    nitrous_size_results = size_tank(volume, nitrous_radius, nitrous_meop, nitrous_safety_factor, 
                                     nitrous_boss_opening, al_yield_strength, fibre_allowable_stress, 
                                     translation_efficiency, fibre_volume_fraction, nitrous_min_liner_thickness, 
                                     liner_elastic_modulus, fibre_elastic_modulus)

    return nitrous_size_results