# Material properties

fibre_allowable_stress = 3.5e9      #Allowable stress of carbon fibre in Pa
translation_efficiency = 0.85       #Efficiency of fibre transfer from winding machine to tank
fibre_volume_fraction = 0.72        #Volume fraction of fibre in composite material
al_yield_strength = 2.7e8       #Maximum yield strength of aluminium in Pa


# General operating conditions
min_temp = 20       #Minimum operating temperature in C
max_temp = 35       #Maximum operating temperature in C
ambient_temp = 30       #Ambient temperature in C

# General Tank Properties (for dome contour plots)

tank_radius = 0.052      #Radius in meters
tank_length = 1         #Length in meters
polar_boss_opening = 0.02       #Radius of polar boss opening in meters
meop = 7e6      #Maximum expected operating pressure in Pa
safety_factor = 3       #Safety factor for tank design

# Nitrous Tank Properties
nitrous_radius = 0.055      #Radius in meters
nitrous_boss_opening = 0.02       #Radius of polar boss opening in meters
nitrous_meop = 7e6      #Maximum expected operating pressure in Pa
nitrous_safety_factor = 3       #Safety factor for tank design
nitrous_ullage_percentage = 10       #Percentage of ullage in the tank

#Nitrogen Tank Properties
bottle_radius = 0.052       #Radius in meters
bottle_boss_opening = 0.02  #Radius of polar boss opening in meters
bottle_safety_factor = 3    #Safety factor for nitrogen bottle
bottle_pressure = 2e7       #Pressure of the nitrogen bottle in Pa
ullage_pressure = 7e6       #Pressure of the ullage in the tank in Pa
regulator_pressure = ullage_pressure      #Regulator set point pressure in Pa
reg_min_margin = 2e6        #Minimum difference between end bottle pressure and regulator pressure in Pa; check from regulator datasheet

# Fluid properties
R_nitrogen = 296.8      #Specific gas constant for nitrogen in J/(kg*K)
nitrous_mass = 7        #Mass of nitrous oxide in the tank in kg

# Boss lengths (minimum thread lengths according to the standard)
nitrous_bosses = {
    "nitrous_forward_boss": 15,
    "nitrous_aft_boss": 19
}
bottle_bosses = {
    "bottle_forward_boss": 15,
    "bottle_aft_boss": 15
}

# Plumbing
plumbing_length = 0.0       #Length of plumbing in meters