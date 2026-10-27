from Inputs import (nitrous_radius, nitrous_mass, nitrous_meop, 
                    nitrous_ullage_percentage, ambient_temp,nitrous_safety_factor, 
                    nitrous_boss_opening, al_yield_strength,fibre_allowable_stress,
                    translation_efficiency, fibre_volume_fraction)
from Geodesic_Dome import dome_contour
import Working_Memory
from COPV_Netting_Analysis import run_netting
from CoolProp.CoolProp import PropsSI, PhaseSI

ambient_temp_K = ambient_temp + 273.15 
bar = 0.00001 * nitrous_meop  # convert Pa to bar

ullage = nitrous_ullage_percentage / 100.0  # convert percentage to fraction

# Calculate the tank length

phase = PhaseSI('P', nitrous_meop, 'T', ambient_temp_K, "NITROUSOXIDE")
rho = PropsSI('D', 'P', nitrous_meop, 'T', ambient_temp_K, "NITROUSOXIDE")  # kg/m^3
volume = nitrous_mass / rho  # m^3
volume = volume + (ullage * volume) #Adding ullage volume

nitrous_contour = dome_contour(nitrous_radius, nitrous_meop, nitrous_safety_factor, nitrous_boss_opening, al_yield_strength)

nitrous_dome_volume = nitrous_contour["dome_volume"]
nitrous_dome_depth = nitrous_contour["dome_depth"]

nitrous_cyl_volume = volume - (2 * nitrous_dome_volume)
nitrous_cyl_length = nitrous_cyl_volume / (3.14159 * nitrous_radius**2)  # m

nitrous_tank_length = nitrous_cyl_length + (2 * nitrous_dome_depth)
Working_Memory.nitrous_tank_length = nitrous_tank_length

nitrous_liner_thickness = nitrous_contour["thickness"]
Working_Memory.nitrous_liner_thickness = nitrous_liner_thickness

#Find thickness and outer radius of the tank

nitrous_overwrap_thickness = run_netting(nitrous_radius, nitrous_meop, nitrous_safety_factor, nitrous_boss_opening, fibre_allowable_stress, translation_efficiency, fibre_volume_fraction, al_yield_strength, "Nitrous Oxide")
nitrous_total_thickness = nitrous_liner_thickness + nitrous_overwrap_thickness

nitrous_outer_radius = nitrous_radius + nitrous_total_thickness

#Print results

print(f"\n{'.' * 50}")
if phase == 'liquid':
    print(f"Nitrous Oxide is in {phase} phase at {ambient_temp}°C and {bar:.2f} bar")
    print(f"Nitrous Cyl length: {nitrous_cyl_length:.4f} m, Density: {rho:.2f} kg/m^3, Volume: {volume:.4f} m^3, Total length (w.o boss): {nitrous_tank_length} m")
else:
    print(f"**WARNING: Nitrous Oxide is in {phase} phase at {ambient_temp}°C and {bar:.2f} bar**")
    print(f"Nitrous Cyl length: {nitrous_cyl_length:.4f} m, Density: {rho:.2f} kg/m^3, Volume: {volume:.4f} m^3, Total length (w.o boss): {nitrous_tank_length} m")

print(f"Thickness of nitrous tank liner: {nitrous_liner_thickness} m ({nitrous_liner_thickness * 1000:.3f} mm)")
print(f"Thickness of nitrous tank overwrap: {nitrous_overwrap_thickness} m ({nitrous_overwrap_thickness * 1000:.3f} mm)")
print(f"Thickness of nitrous tank total: {nitrous_total_thickness} m ({nitrous_total_thickness * 1000:.3f} mm)")
print(f"Outer radius of nitrous tank: {nitrous_outer_radius} m ({nitrous_outer_radius * 1000:.3f} mm)")
