#Netting Analysis for COPV Rocket tank
import math
from Inputs import tank_radius, meop, safety_factor, polar_boss_opening, fibre_allowable_stress, translation_efficiency, fibre_volume_fraction, al_yield_strength, cylinder_length

thickness = (meop * safety_factor *tank_radius) / (al_yield_strength * 2) #m

tank_outer_radius = tank_radius + thickness #m

max_design_pressure = meop * safety_factor #Pa

hoop_load = max_design_pressure * tank_radius #Pa*m
longitudinal_load = (max_design_pressure * tank_radius) / 2 #Pa*m

wind_angle = math.asin(polar_boss_opening / tank_outer_radius) #radians

helical_wind_thickness = longitudinal_load / (fibre_allowable_stress * translation_efficiency * math.cos(wind_angle)**2) #m

hoop_wind_thickness = (hoop_load - longitudinal_load * math.tan(wind_angle)**2) / (fibre_allowable_stress * translation_efficiency) #m

total_wind_thickness = (helical_wind_thickness + hoop_wind_thickness) / fibre_volume_fraction #m

helical_layers_fraction = helical_wind_thickness / (fibre_volume_fraction * total_wind_thickness) #number of helical layers
hoop_layers_fraction = hoop_wind_thickness / (fibre_volume_fraction * total_wind_thickness) #number of hoop layers

print(f"tank_radius: {tank_radius:.4e} m ({tank_radius * 1000:.3f} mm)")
print(f"meop: {meop:.4e} Pa ({meop / 1e6:.2f} MPa)")
print(f"safety_factor: {safety_factor}")
print(f"polar_boss_opening: {polar_boss_opening:.4e} m ({polar_boss_opening * 1000:.3f} mm)")
print(f"fibre_allowable_stress: {fibre_allowable_stress:.4e} Pa ({fibre_allowable_stress / 1e9:.2f} GPa)")
print(f"translation_efficiency: {translation_efficiency}")
print(f"fibre_volume_fraction: {fibre_volume_fraction}")

print(f"max_design_pressure: {max_design_pressure:.4e} Pa ({max_design_pressure / 1e6:.2f} MPa)")

print(f"hoop_load: {hoop_load:.4e} N/m ({hoop_load / 1000:.2f} kN/m)")
print(f"longitudinal_load: {longitudinal_load:.4e} N/m ({longitudinal_load / 1000:.2f} kN/m)")

print(f"wind_angle: {wind_angle:.4e} rad ({math.degrees(wind_angle):.2f}°)")

print(f"helical_wind_thickness: {helical_wind_thickness:.4e} m ({helical_wind_thickness * 1000:.4f} mm)")
print(f"hoop_wind_thickness: {hoop_wind_thickness:.4e} m ({hoop_wind_thickness * 1000:.4f} mm)")
print(f"total_wind_thickness: {total_wind_thickness:.4e} m ({total_wind_thickness * 1000:.4f} mm)")

print(f"helical_fraction: {helical_layers_fraction:.4e} ({helical_layers_fraction * 100:.2f}%)")
print(f"hoop_fraction: {hoop_layers_fraction:.4e} ({hoop_layers_fraction * 100:.2f}%)")

sanity_check = 1.5 * max_design_pressure * tank_outer_radius / (fibre_allowable_stress * translation_efficiency)
print(f"Sanity check: {sanity_check:.4e} m, values should match")
print(f"Total wind thickness * fibre volume fraction: {total_wind_thickness * fibre_volume_fraction:.4e} m")  # should match
