import math

def cyl_volume(
        volume: float, 
        dome_volume: float) -> float:
    return volume - (2 * dome_volume)

def cyl_length(
        volume: float, 
        radius: float) -> float:
    return volume / (math.pi * radius**2)

def tank_length(
        cyl_length: float, 
        dome_depth: float) -> float:
    return cyl_length + (2 * dome_depth)
