def total_system_dimensions(nitrous_tank_length, bottle_length,
                            nitrous_liner_thickness, bottle_liner_thickness,
                            nitrous_bosses, bottle_bosses, plumbing_length):

    # New dicts, so the inputs are left untouched
    nitrous_boss_lengths = {
        name: (1.6 * length / 1000) - nitrous_liner_thickness
        for name, length in nitrous_bosses.items()
    }
    bottle_boss_lengths = {
        name: (1.6 * length / 1000) - bottle_liner_thickness
        for name, length in bottle_bosses.items()
    }

    total_nitrous_length = nitrous_tank_length + sum(nitrous_boss_lengths.values())
    total_bottle_length  = bottle_length + sum(bottle_boss_lengths.values())

    combined_tanks_length = total_nitrous_length + total_bottle_length
    total_system_length   = combined_tanks_length + plumbing_length

    return dict(
        nitrous_boss_lengths  = nitrous_boss_lengths,
        bottle_boss_lengths   = bottle_boss_lengths,
        total_nitrous_length  = total_nitrous_length,
        total_bottle_length   = total_bottle_length,
        combined_tanks_length = combined_tanks_length,
        total_system_length   = total_system_length,
    )