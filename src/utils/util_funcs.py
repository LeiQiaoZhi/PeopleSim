import math
from typing import *


def sigmoid(x: float, mid_point: float = 0, rate: float = 8) -> float:
    '''
    between 0 and 1
    mid point is where output is 0.5
    higher the rate, more gentle the slope
    '''
    return 1 / (1 + math.e ** (-(x-mid_point)/rate))


def find_person_by_id(people, target_id):
    '''
    returns the person with target id or None
    '''
    filtered = list(filter(lambda p: p.id == target_id, people))
    return filtered[0] if len(filtered) > 0 else None
