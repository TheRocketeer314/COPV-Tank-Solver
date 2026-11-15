from Inputs import (ambient_temp, nitrous_mass, nitrous_ullage_percentage, 
                    ullage_pressure, bottle_pressure, regulator_pressure, 
                    R_nitrogen, reg_min_margin, bottle_radius,
                    bottle_boss_opening, bottle_safety_factor,
                    al_yield_strength, fibre_volume_fraction,
                    fibre_allowable_stress, translation_efficiency)
from coolprop_func import (density_TP, density_SP, density_TQ, psat_T,
                           mass_entropy_TP, mass_enthalpy_SP, mass_internal_energy_TP)
from scipy.optimize import brentq
import numpy as np
from volume_tank_sizing import size_tank

T0 = ambient_temp + 273.15  # Convert ambient temperature to Kelvin

# Find nitrous oxide properties

psat = psat_T(T0, 'N2O', 0)  # Saturation pressure at ambient temperature
rho_liquid = density_TQ(T0, 'N2O', 0)  # Density of liquid nitrous oxide at ambient temperature

V_liquid = nitrous_mass / rho_liquid  # Volume of liquid nitrous oxide in m^3
V_u0 = (nitrous_ullage_percentage / 100) * V_liquid  # Initial ullage volume in m^3
V_u1 = V_u0 + V_liquid  #Final ullage volume in m^3

P_end = regulator_pressure + reg_min_margin  # Final pressure in the nitrogen bottle after regulator in Pa

#Nitrogen required for initial pressurization of the tank

p_N2 = ullage_pressure - psat  
m_pad = p_N2 * V_u0 / (R_nitrogen * T0)  # Mass of nitrogen required for initial pressurization in kg

print(f"Nitrogen required for initial pressurisation:   {m_pad} kg")

# Calculate the mean inlet enthalpy of nitrogen from the bottle to the ullage

def mean_inlet_enthalpy(T0, P0, P_end, n=200):
    s0 = mass_entropy_TP(T0, P0, 'N2')
    Ps  = np.linspace(P0, P_end, n)
    rho = np.array([density_SP(s0, p, 'N2') for p in Ps])
    h   = np.array([mass_enthalpy_SP(s0, p, 'N2') for p in Ps])
    dm  = -np.diff(rho)                 # mass leaving per step (per m³ of bottle)
    h_mid = 0.5*(h[:-1] + h[1:])
    return np.sum(h_mid*dm)/np.sum(dm)

h_in = mean_inlet_enthalpy(T0, bottle_pressure, P_end)

# Nitrogen needed to pressurize the ullage from T0 to T2, where T2 is the final ullage temperature after pressurization. The final temperature is found by solving the energy balance equation.

m1 = V_u0 * density_TP(T0, ullage_pressure, 'N2')
u1 = mass_internal_energy_TP(T0, ullage_pressure, 'N2')
def energy_residual(T2):
    m2 = density_TP(T2, ullage_pressure, 'N2')*V_u1
    u2 = mass_internal_energy_TP(T2, ullage_pressure, 'N2')
    return m2*u2 - (m1*u1 + (m2-m1)*h_in - ullage_pressure*V_liquid)
T2 = brentq(energy_residual, 150, 400)
rho_2 = density_TP(T2, ullage_pressure, 'N2')

m2 = rho_2 * V_u1
m_in = m2 - m1
print (f"Nitrogen required for pressurisation during burn:  {m_in} kg")

m_req = m_in + m_pad
m_total = m_req + (0.1 * m_req)  # Add 10% margin for safety
print(f"Total nitrogen delivered (with safety margin):   {m_total} kg")

#Calculate the delivered fraction
s0 = mass_entropy_TP(T0, bottle_pressure, 'N2')
rho_0 = density_TP(T0, bottle_pressure, 'N2')
rho_end = density_SP(s0, P_end, 'N2')
f_delivered = 1 - (rho_end/rho_0)

# Calculate total mass of nitrogen required and the length of the tank needed
m_nitrogen = m_total / f_delivered
print(f"Total nitrogen stored:  {m_nitrogen} kg")
V_nitrogen = m_nitrogen / rho_0
print(f"Volume of nitrogen: {V_nitrogen} m3\n")
nitrogen_size_results = size_tank(V_nitrogen, bottle_radius, bottle_pressure, bottle_safety_factor, bottle_boss_opening, al_yield_strength, fibre_allowable_stress, translation_efficiency, fibre_volume_fraction)

#Print results

print(f"{'.' * 50}")
print(f"Length of nitrogen bottle cylinder:    {nitrogen_size_results['cylinder_length']} m")
print(f"Total length of nitrogen bottle (without boss): {nitrogen_size_results['tank_length']} m")
print(f"Thickness of nitrogen tank liner: {nitrogen_size_results['liner_thickness']} m ({nitrogen_size_results['liner_thickness'] * 1000:.3f} mm)")
print(f"Thickness of nitrogen tank overwrap: {nitrogen_size_results['overwrap_thickness']} m ({nitrogen_size_results['overwrap_thickness'] * 1000:.3f} mm)")
print(f"Thickness of nitrogen tank total: {nitrogen_size_results['total_thickness']} m ({nitrogen_size_results['total_thickness'] * 1000:.3f} mm)")
print(f"Outer radius of nitrogen tank: {nitrogen_size_results['outer_radius']} m ({nitrogen_size_results['outer_radius'] * 1000:.3f} mm)")
