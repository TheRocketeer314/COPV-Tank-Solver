# Tank geometry and material properties

tank_radius = 0.052      #Radius in meters
polar_boss_opening = 0.02       #Radius of polar boss opening in meters
al_yield_strength = 2.7e8       #Maximum yield strength of aluminium in Pa

# Carbon fibre properties

fibre_allowable_stress = 3.5e9      #Allowable stress of carbon fibre in Pa
translation_efficiency = 0.85       #Efficiency of fibre transfer from winding machine to tank
fibre_volume_fraction = 0.72        #Volume fraction of fibre in composite material

# Tank operating conditions
min_temp = 20       #Minimum operating temperature in C
max_temp = 35       #Maximum operating temperature in C
ambient_temp = 30       #Ambient temperature in C
meop = 2e7      #Maximum expected operating pressure in Pa
safety_factor = 3       #Safety factor for tank design
ullage_percentage = 10       #Percentage of ullage in the tank

#Nitrogen Calculations
bottle_pressure = 2e7       #Pressure of the nitrogen bottle in Pa
ullage_pressure = 7e6       #Pressure of the ullage in the tank in Pa
regulator_pressure = ullage_pressure      #Regulator set point pressure in Pa
reg_min_margin = 2e6        #Minimum difference between end bottle pressure and regulator pressure in Pa; check from regulator datasheet

# Fluid properties
nitrous = True      #Select True for nitrous oxide, False for nitrogen
nitrogen = False        #Select True for nitrogen, False for nitrous oxide
R_nitrogen = 296.8      #Specific gas constant for nitrogen in J/(kg*K)
nitrous_mass = 7        #Mass of nitrous oxide in the tank in kg

