import math


def sigmoid(x: float, mid_point: float = 0, rate: float = 8) -> float:
    '''
    between 0 and 1
    mid point is where output is 0.5
    higher the rate, more gentle the slope
    '''
    return 1 / (1 + math.e ** (-(x-mid_point)/rate))
