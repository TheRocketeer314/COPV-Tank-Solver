
from converters import pres_pa_to_bar
from coolprop_func import density_TP, phase_TP
from volume_tank_sizing import size_tank

def nitrous_tank_sizing(nitrous_radius, nitrous_mass, nitrous_meop, 
                        nitrous_ullage_fraction, ambient_temp, ambient_temp_K, nitrous_safety_factor, 
                        nitrous_boss_opening, al_yield_strength,fibre_allowable_stress,
                        translation_efficiency, fibre_volume_fraction):
    
    bar = pres_pa_to_bar(nitrous_meop)  # convert Pa to bar

    ullage = nitrous_ullage_fraction

    # Calculate the tank length

    phase = phase_TP(ambient_temp_K, nitrous_meop, "NITROUSOXIDE")
    rho = density_TP(ambient_temp_K, nitrous_meop, "NITROUSOXIDE")  # kg/m^3
    volume = nitrous_mass / rho  # m^3
    volume = volume + (volume / (1 - ullage)) #Adding ullage volume

    nitrous_size_results = size_tank(volume, nitrous_radius, nitrous_meop, nitrous_safety_factor, nitrous_boss_opening, al_yield_strength, fibre_allowable_stress, translation_efficiency, fibre_volume_fraction)

    return nitrous_size_results