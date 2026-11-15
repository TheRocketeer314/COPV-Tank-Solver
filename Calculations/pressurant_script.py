from Calculations.volume_tank_sizing import size_tank
from Calculations.nitrogen_functions import nitrogen_required, nitrogen_bottle_volume

def bottle_sizing(ambient_temp, nitrous_mass, nitrous_ullage_fraction, ullage_pressure, 
                  bottle_pressure, regulator_pressure, reg_min_margin, R_nitrogen, bottle_radius, 
                  bottle_safety_factor, bottle_boss_opening, al_yield_strength, fibre_allowable_stress, 
                  translation_efficiency, fibre_volume_fraction):
    
    nitrogen_required_results = nitrogen_required(ambient_temp, nitrous_mass, nitrous_ullage_fraction, 
                                                ullage_pressure, bottle_pressure, regulator_pressure, 
                                                reg_min_margin, R_nitrogen, margin=0.10)

    nitrogen_bottle_volume_results = nitrogen_bottle_volume(nitrogen_required_results['m_delivered'], 
                                                            ambient_temp, bottle_pressure, 
                                                            nitrogen_required_results['p_end'])

    nitrogen_size_results = size_tank(nitrogen_bottle_volume_results['volume'], bottle_radius, 
                                    bottle_pressure, bottle_safety_factor, bottle_boss_opening, 
                                    al_yield_strength, fibre_allowable_stress, translation_efficiency, 
                                    fibre_volume_fraction)

    return {
        **nitrogen_size_results,           # tank_length, liner_thickness, ...
        **nitrogen_required_results,       # m_pad, m_burn, m_delivered, T_ullage_final, p_end
        **nitrogen_bottle_volume_results,  # f_delivered, m_stored, volume
    }
