from Inputs import ambient_temp, nitrous_mass, ullage_percentage, ullage_pressure, bottle_pressure, regulator_pressure, R_nitrogen, reg_min_margin, tank_radius
from CoolProp.CoolProp import PropsSI as PS
from scipy.optimize import brentq
import numpy as np

T0 = ambient_temp + 273.15  # Convert ambient temperature to Kelvin

# Find nitrous oxide properties

psat = PS('P', 'T', T0, 'Q', 0, 'N2O')  # Saturation pressure at ambient temperature
rho_liquid = PS('D', 'T', T0, 'Q', 0, 'N2O')  # Density of liquid nitrous oxide at ambient temperature

V_liquid = nitrous_mass / rho_liquid  # Volume of liquid nitrous oxide in m^3
V_u0 = (ullage_percentage / 100) * V_liquid  # Initial ullage volume in m^3
V_u1 = V_u0 + V_liquid  #Final ullage volume in m^3

P_end = regulator_pressure + reg_min_margin  # Final pressure in the nitrogen bottle after regulator in Pa

#Nitrogen required for initial pressurization of the tank

p_N2 = ullage_pressure - psat  
m_pad = p_N2 * V_u0 / (R_nitrogen * T0)  # Mass of nitrogen required for initial pressurization in kg

print(f"Nitrogen required for initial pressurisation:   {m_pad} kg")

# Calculate the mean inlet enthalpy of nitrogen from the bottle to the ullage

def mean_inlet_enthalpy(T0, P0, P_end, n=200):
    s0 = PS('S','T',T0,'P',P0,'N2')
    Ps  = np.linspace(P0, P_end, n)
    rho = np.array([PS('D','S',s0,'P',p,'N2') for p in Ps])
    h   = np.array([PS('H','S',s0,'P',p,'N2') for p in Ps])
    dm  = -np.diff(rho)                 # mass leaving per step (per m³ of bottle)
    h_mid = 0.5*(h[:-1] + h[1:])
    return np.sum(h_mid*dm)/np.sum(dm)

h_in = mean_inlet_enthalpy(T0, bottle_pressure, P_end)
T_in_equiv = PS('T','H',h_in,'P',ullage_pressure,'N2')

# Nitrogen needed to pressurize the ullage from T0 to T2, where T2 is the final ullage temperature after pressurization. The final temperature is found by solving the energy balance equation.

m1 = V_u0 * PS('D','T',T0,'P',ullage_pressure,'N2')
u1 = PS('U','T',T0,'P',ullage_pressure,'N2')
def energy_residual(T2):
    m2 = PS('D','T',T2,'P',ullage_pressure,'N2')*V_u1
    u2 = PS('U','T',T2,'P',ullage_pressure,'N2')
    return m2*u2 - (m1*u1 + (m2-m1)*h_in - ullage_pressure*V_liquid)
T2 = brentq(energy_residual, 150, 400)
rho_2 = PS('D','T',T2,'P',ullage_pressure,'N2')

m2 = rho_2 * V_u1
m_in = m2 - m1
print (f"Nitrogen required for pressurisation during burn:  {m_in} kg")

m_req = m_in + m_pad
m_total = m_req + (0.1 * m_req)  # Add 10% margin for safety
print(f"Total nitrogen delivered (with safety margin):   {m_total} kg")

#Calculate the delivered fraction
s0 = PS('S','T', T0,'P',bottle_pressure,'N2')
rho_0 = PS('D', 'T', T0, 'P', bottle_pressure, 'N2')
rho_end = PS('D', 'S', s0, 'P', P_end, "N2")
f_delivered = 1 - (rho_end/rho_0)

# Calculate total mass of nitrogen required and the length of the tank needed
m_nitrogen = m_total / f_delivered
print(f"Total nitrogen stored:  {m_nitrogen} kg")
V_nitrogen = m_nitrogen / rho_0
print(f"Volume of nitrogen: {V_nitrogen} m3")
tank_length = V_nitrogen / (3.14159 * tank_radius**2)  # m
print(f"Length of nitrogen tank:    {tank_length} m")
