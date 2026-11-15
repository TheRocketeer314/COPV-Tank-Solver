from Calculations.coolprop_functions import (density_SP, density_TQ, mass_enthalpy_SP, 
                           mass_entropy_TP, mass_internal_energy_TP, 
                           density_TP, psat_T)
import numpy as np
from scipy.optimize import brentq
from Calculations.converters import temp_C_to_K

def mean_inlet_enthalpy(T0, P0, P_end, n=200):
    s0 = mass_entropy_TP(T0, P0, 'N2')
    Ps  = np.linspace(P0, P_end, n)
    rho = np.array([density_SP(s0, p, 'N2') for p in Ps])
    h   = np.array([mass_enthalpy_SP(s0, p, 'N2') for p in Ps])
    dm  = -np.diff(rho)                 # mass leaving per step (per m³ of bottle)
    h_mid = 0.5*(h[:-1] + h[1:])
    return np.sum(h_mid*dm)/np.sum(dm)

def burn_gas_mass(T0, v_u0, v_liq, p_ullage, h_in):
    v_u1 = v_u0 + v_liq
    m1   = v_u0 * density_TP(T0, p_ullage, "N2")
    u1   = mass_internal_energy_TP(T0, p_ullage, "N2")

    def residual(T2):
        m2 = density_TP(T2, p_ullage, "N2") * v_u1
        u2 = mass_internal_energy_TP(T2, p_ullage, "N2")
        return m2*u2 - (m1*u1 + (m2 - m1)*h_in - p_ullage*v_liq)

    T2     = brentq(residual, 150, 400)
    m_burn = density_TP(T2, p_ullage, "N2") * v_u1 - m1
    return m_burn, T2

def nitrogen_required(ambient_temp, m_n2o, ullage_fraction, p_ullage, p_bottle,
                      p_reg, reg_margin, r_n2, margin=0.10):
    T0 = temp_C_to_K(ambient_temp)
    p_sat = psat_T(T0, "NITROUSOXIDE")
    v_liq = m_n2o / density_TP(T0, p_ullage,"NITROUSOXIDE")
    v_u0  = (ullage_fraction * v_liq) / (1 - ullage_fraction)
    p_end = p_reg + reg_margin

    m_pad        = (p_ullage - p_sat) * v_u0 / (r_n2 * T0)
    h_in         = mean_inlet_enthalpy(T0, p_bottle, p_end)
    m_burn, T2   = burn_gas_mass(T0, v_u0, v_liq, p_ullage, h_in)
    m_delivered  = (m_pad + m_burn) * (1 + margin)

    return dict(m_pad=m_pad, m_burn=m_burn, m_delivered=m_delivered,
                T_ullage_final=T2, p_end=p_end)

def nitrogen_bottle_volume(m_delivered, ambient_temp, p_bottle, p_end):
    T0 = temp_C_to_K(ambient_temp)
    s0       = mass_entropy_TP(T0, p_bottle, "N2")
    rho_0    = density_TP(T0, p_bottle, "N2")
    rho_end  = density_SP(s0, p_end, "N2")
    f_deliv  = 1 - rho_end / rho_0

    m_stored = m_delivered / f_deliv
    return dict(f_delivered=f_deliv, m_stored=m_stored,
                volume=m_stored / rho_0)