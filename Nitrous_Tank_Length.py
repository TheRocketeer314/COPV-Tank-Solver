from Inputs import tank_radius, nitrous, nitrous_mass, nitrogen, meop, ullage_percentage, ambient_temp
from CoolProp.CoolProp import PropsSI, PhaseSI

ambient_temp_K = ambient_temp + 273.15 
bar = 0.00001 * meop  # convert Pa to bar

ullage = ullage_percentage / 100.0  # convert percentage to fraction

# Confirm that only one of nitrous or nitrogen is selected

if (nitrous and nitrogen) or (not nitrous and not nitrogen):
    raise ValueError("Please select either nitrous or nitrogen, but not both.")

# Calculate the tank length

phase = PhaseSI('P', meop, 'T', ambient_temp_K, "N20")
rho = PropsSI('D', 'P', meop, 'T', ambient_temp_K, "N20")  # kg/m^3
volume = nitrous_mass / rho  # m^3
volume = volume + (ullage * volume) #Adding ullage volume
tank_length = volume / (3.14159 * tank_radius**2)  # m

# Print the results

if phase == 'liquid':
    print(f"Nitrous Oxide is in {phase} phase at {ambient_temp}°C and {bar:.2f} bar")
    print(f"Tank length: {tank_length:.4f} m, Density: {rho:.2f} kg/m^3, Volume: {volume:.4f} m^3")
else:
    print(f"**WARNING: Nitrous Oxide is in {phase} phase at {ambient_temp}°C and {bar:.2f} bar**")
    print(f"Tank length: {tank_length:.4f} m, Density: {rho:.2f} kg/m^3, Volume: {volume:.4f} m^3")