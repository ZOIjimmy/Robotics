import math


def calculateTurnAngle(cup_x, cup_y):
    dot = -(cup_y-190)
    cos = dot / ((cup_x - 620)**2 + (cup_y - 190)**2)**0.5
    degree = math.degrees(math.acos(cos))
    return degree
    