import numpy as np

def predictCupHeight(x, y, height_in_pixel):
    # calculate parallel distance to origin in robot coord unit
    p_z = y * (2 ** 0.5) + (x - y) / (2 ** 0.5)
    # in cm
    # p_dis = 0.0971 * p_z + 15.201
    p_dis = 0.0971 * p_z + 5.0

    ratio = 0.0016 * p_dis + 0.0064
    offset = 1.9041 * np.log(p_dis) - 9.4356

    cup_height = ratio * height_in_pixel + offset
    
    return cup_height
    
