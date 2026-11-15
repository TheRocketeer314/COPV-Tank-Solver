from COPV_Netting_Analysis import run_netting, radii_from_outer
from Inputs import tank_radius, meop, safety_factor, polar_boss_opening, fibre_allowable_stress, translation_efficiency, fibre_volume_fraction, al_yield_strength

print("Tank radius from Inputs.py:", tank_radius)

results = radii_from_outer(tank_radius, meop, safety_factor, polar_boss_opening, fibre_allowable_stress, translation_efficiency, fibre_volume_fraction, al_yield_strength)
inner_radius = results["r_in"]
print("Tank inner radius from new script:", inner_radius)

outer_radius = run_netting(inner_radius, meop, safety_factor, polar_boss_opening, fibre_allowable_stress, translation_efficiency, fibre_volume_fraction, al_yield_strength, "Test Fluid")
print("Tank outer radius from og script:", outer_radius)
print("Difference:", outer_radius - tank_radius)
print("Accuracy:", (outer_radius / tank_radius) * 100, "%")
