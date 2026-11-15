#Netting Analysis for COPV Rocket tank
import math
from results_table import print_table

def run_netting(tank_radius, meop, safety_factor, polar_boss_opening, fibre_allowable_stress, translation_efficiency, fibre_volume_fraction, al_yield_strength, fluid):
    thickness = (meop * safety_factor * tank_radius) / (al_yield_strength * 2) #m

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

    print_table(
        f"{fluid} Tank Parameters",
        [
            ("Tank Radius", f"{tank_radius:.4e} m", f"{tank_radius * 1000:.3f} mm"),
            ("MEOP", f"{meop:.4e} Pa", f"{meop / 1e6:.2f} MPa"),
            ("Safety Factor", f"{safety_factor}", ""),
            ("Polar Boss Opening", f"{polar_boss_opening:.4e} m", f"{polar_boss_opening * 1000:.3f} mm"),
            ("Fibre Allowable Stress", f"{fibre_allowable_stress:.4e} Pa", f"{fibre_allowable_stress / 1e9:.2f} GPa"),
            ("Translation Efficiency", f"{translation_efficiency:.4f}", ""),
            ("Fibre Volume Fraction", f"{fibre_volume_fraction:.4f}", f"{fibre_volume_fraction * 100:.2f}%"),

            ("Max Design Pressure", f"{max_design_pressure:.4e} Pa", f"{max_design_pressure / 1e6:.2f} MPa"),

            ("Hoop Load", f"{hoop_load:.4e} N/m", f"{hoop_load / 1000:.2f} kN/m"),
            ("Longitudinal Load", f"{longitudinal_load:.4e} N/m", f"{longitudinal_load / 1000:.2f} kN/m"),
            ("Wind Angle", f"{wind_angle:.4e} rad", f"{math.degrees(wind_angle):.2f}°"),

            ("Helical Wind Thickness", f"{helical_wind_thickness:.4e} m", f"{helical_wind_thickness * 1000:.4f} mm"),
            ("Hoop Wind Thickness", f"{hoop_wind_thickness:.4e} m", f"{hoop_wind_thickness * 1000:.4f} mm"),
            ("Total Wind Thickness", f"{total_wind_thickness:.4e} m", f"{total_wind_thickness * 1000:.4f} mm"),

            ("Helical Layers Fraction", f"{helical_layers_fraction:.4e}", f"{helical_layers_fraction * 100:.2f}%"),
            ("Hoop Layers Fraction", f"{hoop_layers_fraction:.4e}", f"{hoop_layers_fraction * 100:.2f}%"),
        ]
    )

    return total_wind_thickness
