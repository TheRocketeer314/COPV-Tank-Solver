from CoolProp.CoolProp import PropsSI as PS
from CoolProp.CoolProp import PhaseSI

def density_TP(
        T: float,   # Temperature in Kelvin
        P: float,   #Pressure in Pa
        fluid: str  #Fluid name (e.g., 'N2O', 'N2', etc.)
        ) -> float:
    return PS('D', 'T', T, 'P', P, fluid)

def density_TQ(
        T: float,   # Temperature in Kelvin
        fluid: str,  # Fluid name (e.g., 'N2O', 'N2', etc.)
        Q: float = 0   # Quality (0 for saturated liquid, 1 for saturated vapor)
        ) -> float:
    return PS('D', 'T', T, 'Q', Q, fluid)

def density_SP(
        S: float,   # Entropy in J/(kg*K)
        P: float,   # Pressure in Pa
        fluid: str  # Fluid name (e.g., 'N2O', 'N2', etc.)
        ) -> float:
    return PS('D', 'S', S, 'P', P, fluid)

def psat_T(
        T: float,   # Temperature in Kelvin
        fluid: str,  # Fluid name (e.g., 'N2O', 'N2', etc.)
        Q: float = 0   # Quality (0 for saturated liquid, 1 for saturated vapor)
        ) -> float:
    return PS('P', 'T', T, 'Q', Q, fluid)

def mass_entropy_TP(
        T: float,   # Temperature in Kelvin
        P: float,   # Pressure in Pa
        fluid: str  # Fluid name (e.g., 'N2O', 'N2', etc.)
        ) -> float:
    return PS('S', 'T', T, 'P', P, fluid)

def mass_enthalpy_SP(
        S: float,   # Entropy in J/(kg*K)
        P: float,   # Pressure in Pa
        fluid: str  # Fluid name (e.g., 'N2O', 'N2', etc.)
        ) -> float:
    return PS('H', 'S', S, 'P', P, fluid)

def mass_internal_energy_TP(
        T: float,   # Temperature in Kelvin
        P: float,   # Pressure in Pa
        fluid: str  # Fluid name (e.g., 'N2O', 'N2', etc.)
        ) -> float:
    return PS('U', 'T', T, 'P', P, fluid)

def phase_TP(
        T: float,   # Temperature in Kelvin
        P: float,   # Pressure in Pa
        fluid: str  # Fluid name (e.g., 'N2O', 'N2', etc.)
        ) -> str:
    return PhaseSI('P', P, 'T', T, fluid)