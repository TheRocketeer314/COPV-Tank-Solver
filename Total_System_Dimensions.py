from Inputs import nitrous_bosses, bottle_bosses, plumbing_length
from Working_Memory import nitrous_tank_length, nitrous_liner_thickness, bottle_length, bottle_liner_thickness

for boss in nitrous_bosses:
    boss_length = nitrous_bosses[boss]
    nitrous_bosses[boss] = (1.6 * boss_length / 1000) - nitrous_liner_thickness

for boss in bottle_bosses:
    boss_length = bottle_bosses[boss]
    bottle_bosses[boss] = (1.6 * boss_length / 1000) - bottle_liner_thickness

total_nitrous_tank_length = nitrous_tank_length + sum(nitrous_bosses.values())
total_bottle_length = bottle_length + sum(bottle_bosses.values())

combined_tanks_length = total_nitrous_tank_length + total_bottle_length

print(f"The total lengths of the tanks (without plumbing): {combined_tanks_length} m")

total_system_length = combined_tanks_length + plumbing_length

print (f"The total length of the tank system (with plumbing): {total_system_length} m")