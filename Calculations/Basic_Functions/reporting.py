from pathlib import Path
from Calculations.Basic_Functions.results_table import print_table

def next_results_file(folder="results"):
    Path(folder).mkdir(exist_ok=True)
    i = 1
    while (Path(folder) / f"results_{i:03d}.txt").exists():
        i += 1
    return Path(folder) / f"results_{i:03d}.txt"

def report(inputs, nitrous, bottle, system):
    i = inputs

    print_table("Inputs: operating conditions", [
        ("Ambient temperature",  f"{i['ambient_temp']:.1f} °C",  f"{i['ambient_temp'] + 273.15:.2f} K"),
        ("Min temperature",      f"{i['min_temp']:.1f} °C",      f"{i['min_temp'] + 273.15:.2f} K"),
        ("Max temperature",      f"{i['max_temp']:.1f} °C",      f"{i['max_temp'] + 273.15:.2f} K"),
    ])

    print_table("Inputs: nitrous tank", [
        ("Outer radius",     f"{i['nitrous_radius']:.4f} m",        f"{i['nitrous_radius']*1000:.1f} mm"),
        ("Nitrous mass",     f"{i['nitrous_mass']:.3f} kg",         ""),
        ("MEOP",             f"{i['nitrous_meop']:.4e} Pa",         f"{i['nitrous_meop']/1e5:.1f} bar"),
        ("Safety factor",    f"{i['nitrous_safety_factor']}",       ""),
        ("Ullage fraction",  f"{i['nitrous_ullage_fraction']:.3f}", f"{i['nitrous_ullage_fraction']*100:.1f} %"),
        ("Boss opening",     f"{i['nitrous_boss_opening']:.4f} m",  f"{i['nitrous_boss_opening']*1000:.1f} mm"),
    ])

    print_table("Inputs: nitrogen bottle", [
        ("Outer radius",       f"{i['bottle_radius']:.4f} m",        f"{i['bottle_radius']*1000:.1f} mm"),
        ("Bottle pressure",    f"{i['bottle_pressure']:.4e} Pa",     f"{i['bottle_pressure']/1e5:.1f} bar"),
        ("Regulator setpoint", f"{i['regulator_pressure']:.4e} Pa",  f"{i['regulator_pressure']/1e5:.1f} bar"),
        ("Min reg margin",     f"{i['reg_min_margin']:.4e} Pa",      f"{i['reg_min_margin']/1e5:.1f} bar"),
        ("Safety factor",      f"{i['bottle_safety_factor']}",       ""),
        ("Boss opening",       f"{i['bottle_boss_opening']:.4f} m",  f"{i['bottle_boss_opening']*1000:.1f} mm"),
    ])

    print_table("Inputs: materials", [
        ("Al yield strength",     f"{i['al_yield_strength']:.4e} Pa",     f"{i['al_yield_strength']/1e6:.0f} MPa"),
        ("Fibre allowable",       f"{i['fibre_allowable_stress']:.4e} Pa", f"{i['fibre_allowable_stress']/1e9:.2f} GPa"),
        ("Translation eff.",      f"{i['translation_efficiency']:.2f}",    ""),
        ("Fibre volume fraction", f"{i['fibre_volume_fraction']:.2f}",     f"{i['fibre_volume_fraction']*100:.0f} %"),
    ])

    print_table("Nitrous tank", [
        ("Total length",       f"{nitrous['tank_length']:.4f} m",       f"{nitrous['tank_length']*1000:.1f} mm"),
        ("Cylinder length",    f"{nitrous['cylinder_length']:.4f} m",   f"{nitrous['cylinder_length']*1000:.1f} mm"),
        ("Tank outer radius",  f"{nitrous['tank_outer_radius']:.4f} m", f"{nitrous['tank_outer_radius']*1000:.1f} mm"),
        ("Tank inner radius",  f"{nitrous['tank_inner_radius']:.4f} m", f"{nitrous['tank_inner_radius']*1000:.1f} mm"),
        ("Liner thickness",    f"{nitrous['liner_thickness']:.4e} m",   f"{nitrous['liner_thickness']*1000:.3f} mm"),
        ("Overwrap thickness", f"{nitrous['overwrap_thickness']:.4e} m", f"{nitrous['overwrap_thickness']*1000:.3f} mm"),
        ("Tank mass",          f"{nitrous['total_mass']:.3f} kg",         ""),
        ("Liner Mass",          f"{nitrous['liner_mass']:.3f} kg",         ""),
        ("Overwrap Mass",          f"{nitrous['overwrap_mass']:.3f} kg",         ""),
    ])
    print_table("Nitrogen bottle", [
        ("Total length",       f"{bottle['tank_length']:.4f} m",        f"{bottle['tank_length']*1000:.1f} mm"),
        ("Cylinder length",    f"{bottle['cylinder_length']:.4f} m",    f"{bottle['cylinder_length']*1000:.1f} mm"),
        ("Tank outer radius",  f"{bottle['tank_outer_radius']:.4f} m",  f"{bottle['tank_outer_radius']*1000:.1f} mm"),
        ("Tank inner radius",  f"{bottle['tank_inner_radius']:.4f} m", f"{bottle['tank_inner_radius']*1000:.1f} mm"),
        ("Liner thickness",    f"{bottle['liner_thickness']:.4e} m",    f"{bottle['liner_thickness']*1000:.3f} mm"),
        ("Overwrap thickness", f"{bottle['overwrap_thickness']:.4e} m", f"{bottle['overwrap_thickness']*1000:.3f} mm"),
        ("Tank mass",          f"{bottle['total_mass']:.3f} kg",         ""),
        ("Liner Mass",          f"{bottle['liner_mass']:.3f} kg",         ""),
        ("Overwrap Mass",          f"{bottle['overwrap_mass']:.3f} kg",         ""),
    ])
    print_table("Nitrogen requirement", [
        ("Pad gas mass",        f"{bottle['m_pad']:.4f} kg",       ""),
        ("Burn gas mass",       f"{bottle['m_burn']:.4f} kg",      ""),
        ("Delivered N2 (+10%)", f"{bottle['m_delivered']:.4f} kg", ""),
        ("Stored N2 in bottle", f"{bottle['m_stored']:.4f} kg",    ""),
        ("Bottle volume",       f"{bottle['volume']:.6f} m³",      f"{bottle['volume']*1000:.3f} L"),
        ("Final ullage temp",   f"{bottle['T_ullage_final']:.2f} K", ""),
    ])

    print_table("Total system length", [
        ("Nitrous tank + bosses", f"{system['total_nitrous_length']:.4f} m",  ""),
        ("N2 bottle + bosses",    f"{system['total_bottle_length']:.4f} m",   ""),
        ("Tanks combined",        f"{system['combined_tanks_length']:.4f} m", ""),
        ("With plumbing",         f"{system['total_system_length']:.4f} m",   ""),
        ("Total system mass",     f"{system['total_system_mass']:.3f} kg",    ""),
    ])