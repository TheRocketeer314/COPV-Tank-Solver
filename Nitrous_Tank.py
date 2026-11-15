
from converters import pres_pa_to_bar
from coolprop_func import density_TP
from volume_tank_sizing import size_tank
from converters import temp_C_to_K

def nitrous_tank_sizing(nitrous_radius, nitrous_mass, nitrous_meop, 
                        nitrous_ullage_fraction, ambient_temp, nitrous_safety_factor, 
                        nitrous_boss_opening, al_yield_strength,fibre_allowable_stress,
                        translation_efficiency, fibre_volume_fraction):
    
    bar = pres_pa_to_bar(nitrous_meop)  # convert Pa to bar

    ullage = nitrous_ullage_fraction

    # Calculate the tank length

    ambient_temp_K = temp_C_to_K(ambient_temp)
    rho = density_TP(ambient_temp_K, nitrous_meop, "NITROUSOXIDE")  # kg/m^3
    volume = nitrous_mass / rho  # m^3
    volume = volume + (volume / (1 - ullage)) #Adding ullage volume

    nitrous_size_results = size_tank(volume, nitrous_radius, nitrous_meop, nitrous_safety_factor, nitrous_boss_opening, al_yield_strength, fibre_allowable_stress, translation_efficiency, fibre_volume_fraction)

    return nitrous_size_results