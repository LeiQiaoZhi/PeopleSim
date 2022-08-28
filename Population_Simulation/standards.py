from __future__ import annotations
import math
from attributes import *
from typing import Callable
import random


class HeightStandard:
    '''
    has a score_fn field
    which is a function that takes in height
        and returns a score between 0 and 1
    '''

    def __init__(
            self,
            score_fn: Callable[[float], float],
            std_name: str = "custom") -> None:
        self.score_fn = score_fn
        self.std_name = std_name

    @staticmethod
    def get_random_height_std(
            basic_attrs: BasicAttributes,
            physical_attrs: PhysicalAttributes) -> HeightStandard:
        '''
        Male: 
            20% no height std
            40% lower the better
            20% must lower than self
            20% heigher the better
        Female:
            20% no height std
            40% higher the better
            20% must higher than self
            20% lower the better
        '''
        gender = basic_attrs.gender
        if gender == 'Male':
            stds = [
                HeightStandard.NO_HEIGHT_STANDARD(),
                HeightStandard.LOWER_THE_BETTER(physical_attrs.height),
                HeightStandard.MUST_BELOW_HEIGHT(physical_attrs.height),
                HeightStandard.HIGHER_THE_BETTER(physical_attrs.height),
            ]
            weights = [0.2, 0.4, 0.2, 0.2]

        elif gender == 'Female':
            stds = [
                HeightStandard.NO_HEIGHT_STANDARD(),
                HeightStandard.HIGHER_THE_BETTER(physical_attrs.height),
                HeightStandard.MUST_ABOVE_HEIGHT(physical_attrs.height),
                HeightStandard.LOWER_THE_BETTER(physical_attrs.height),
            ]
            weights = [0.2, 0.4, 0.2, 0.2]
        else:
            stds = [
                HeightStandard.NO_HEIGHT_STANDARD(),
                HeightStandard.HIGHER_THE_BETTER(physical_attrs.height),
                HeightStandard.LOWER_THE_BETTER(physical_attrs.height),
                HeightStandard.MUST_BELOW_HEIGHT(physical_attrs.height),
                HeightStandard.MUST_ABOVE_HEIGHT(physical_attrs.height),
            ]
            weights = [0.2, 0.2, 0.2, 0.2, 0.2]

        std = random.choices(stds, weights=weights)
        return std[0]

    # region some common default hard standards
    @staticmethod
    def HIGHER_THE_BETTER(half_score_height):
        '''
        half_score_height is the height that can achieve 0.5
        '''
        def fn(height): return height / (height + half_score_height)
        return HeightStandard(fn, "higher the better")

    @staticmethod
    def LOWER_THE_BETTER(half_score_height):
        '''
        half_score_height is the height that can achieve 0.5
        '''
        def fn(height):
            h = max(2 * half_score_height - height, 0)
            return h / (h + half_score_height)
        return HeightStandard(fn, "lower the better")

    @staticmethod
    def MUST_ABOVE_HEIGHT(min_height):
        def fn(height): return int(height >= min_height)
        return HeightStandard(fn, f"must above {min_height} cm")

    @staticmethod
    def MUST_BELOW_HEIGHT(max_height):
        def fn(height): return int(height <= max_height)
        return HeightStandard(fn, f"must below {max_height} cm")

    @staticmethod
    def MUST_BETWEEN_HEIGHT(min_height, max_height):
        def fn(height): return int(height >= min_height
                                   and height <= max_height)
        return HeightStandard(fn, f"must between {min_height} and {max_height} cm")

    @staticmethod
    def NO_HEIGHT_STANDARD():
        def fn(height): return 1
        return HeightStandard(fn, "indifferent")
    # endregion


class PartnerStandards:
    def __init__(
            self,
            height_std: HeightStandard) -> None:
        self.height_std = height_std

    def score(self, candidate) -> float:
        '''
        calculate a score of the candidate
        base on various standards
        '''
        height_score = self.height_std.score_fn(
            candidate.physical_attrs.height)
        # TODO: finish score fn

    @staticmethod
    def generate_random_partner_standards(
            basic_attrs: BasicAttributes,
            physical_attrs: PhysicalAttributes):
        height_std = HeightStandard.get_random_height_std(
            basic_attrs, physical_attrs)
        return PartnerStandards(height_std)
