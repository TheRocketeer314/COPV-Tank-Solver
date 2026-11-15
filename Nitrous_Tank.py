
from converters import pres_pa_to_bar
from coolprop_func import density_TP, phase_TP
from volume_tank_sizing import size_tank

def nitrous_tank_sizing(nitrous_radius, nitrous_mass, nitrous_meop, 
                        nitrous_ullage_percentage, ambient_temp, ambient_temp_K, nitrous_safety_factor, 
                        nitrous_boss_opening, al_yield_strength,fibre_allowable_stress,
                        translation_efficiency, fibre_volume_fraction):
    
    bar = pres_pa_to_bar(nitrous_meop)  # convert Pa to bar

    ullage = nitrous_ullage_percentage / 100.0  # convert percentage to fraction

    # Calculate the tank length

    phase = phase_TP(ambient_temp_K, nitrous_meop, "NITROUSOXIDE")
    rho = density_TP(ambient_temp_K, nitrous_meop, "NITROUSOXIDE")  # kg/m^3
    volume = nitrous_mass / rho  # m^3
    volume = volume + (volume / (1 - ullage)) #Adding ullage volume

    nitrous_size_results = size_tank(volume, nitrous_radius, nitrous_meop, nitrous_safety_factor, nitrous_boss_opening, al_yield_strength, fibre_allowable_stress, translation_efficiency, fibre_volume_fraction)

    #Print results

    print(f"{'.' * 50}")
    if phase == 'liquid':
        print(f"Nitrous Oxide is in {phase} phase at {ambient_temp}°C and {bar:.2f} bar")
        print(f"Nitrous Cyl length: {nitrous_size_results['cylinder_length']:.4f} m, Density: {rho:.2f} kg/m^3, Volume: {volume:.4f} m^3, Total length (w.o boss): {nitrous_size_results['tank_length']} m")
    else:
        print(f"**WARNING: Nitrous Oxide is in {phase} phase at {ambient_temp}°C and {bar:.2f} bar**")
        print(f"Nitrous Cyl length: {nitrous_size_results['cylinder_length']:.4f} m, Density: {rho:.2f} kg/m^3, Volume: {volume:.4f} m^3, Total length (w.o boss): {nitrous_size_results['tank_length']} m")

    print(f"Thickness of nitrous tank liner: {nitrous_size_results['total_thickness'] * 0.5} m ({nitrous_size_results['total_thickness'] * 500:.3f} mm)")
    print(f"Thickness of nitrous tank overwrap: {nitrous_size_results['total_thickness'] * 0.5} m ({nitrous_size_results['total_thickness'] * 500:.3f} mm)")
    print(f"Thickness of nitrous tank total: {nitrous_size_results['total_thickness']} m ({nitrous_size_results['total_thickness'] * 1000:.3f} mm)")
    print(f"Outer radius of nitrous tank: {nitrous_radius + nitrous_size_results['total_thickness']} m ({(nitrous_radius + nitrous_size_results['total_thickness']) * 1000:.3f} mm)")
