from pathlib import Path
from results_table import print_table

def next_results_file(folder="results"):
    Path(folder).mkdir(exist_ok=True)
    i = 1
    while (Path(folder) / f"results_{i:03d}.txt").exists():
        i += 1
    return Path(folder) / f"results_{i:03d}.txt"

def report(nitrous, bottle, system):
    print_table("Nitrous tank", [
        ("Total length",       f"{nitrous['tank_length']:.4f} m",       f"{nitrous['tank_length']*1000:.1f} mm"),
        ("Cylinder length",    f"{nitrous['cylinder_length']:.4f} m",   f"{nitrous['cylinder_length']*1000:.1f} mm"),
        ("Liner thickness",    f"{nitrous['liner_thickness']:.4e} m",   f"{nitrous['liner_thickness']*1000:.3f} mm"),
        ("Overwrap thickness", f"{nitrous['overwrap_thickness']:.4e} m", f"{nitrous['overwrap_thickness']*1000:.3f} mm"),
    ])
    print_table("Nitrogen bottle", [
        ("Total length",       f"{bottle['tank_length']:.4f} m",        f"{bottle['tank_length']*1000:.1f} mm"),
        ("Liner thickness",    f"{bottle['liner_thickness']:.4e} m",    f"{bottle['liner_thickness']*1000:.3f} mm"),
        ("Overwrap thickness", f"{bottle['overwrap_thickness']:.4e} m", f"{bottle['overwrap_thickness']*1000:.3f} mm"),
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
    ])