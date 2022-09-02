from __future__ import annotations
import math
from attributes import *
from typing import Callable
import random
import utils.util_funcs as U


class Standard:
    def __init__(
            self,
            score_fn: Callable[[any, float], float],
            std_name: str = "custom") -> None:
        '''
        score_fn (self:Person, other person's trait) -> score
        '''
        self.score_fn = score_fn
        self.std_name = std_name

# TODO: Gender Standard


class AttractivenessStandard(Standard):
    @staticmethod
    def generate_random_std():
        stds = [
            AttractivenessStandard.INDIFFERNT(),
            AttractivenessStandard.LINEAR_HIGHER_THE_BETTER(),
            AttractivenessStandard.SIMILAR_THE_BETTER(),
            AttractivenessStandard.HIGH_STANDARD(),
        ]
        weights = [0.1, 0.4, 0.4, 0.1]
        std = random.choices(stds, weights=weights)
        return std[0]

    @staticmethod
    def INDIFFERNT():
        return AttractivenessStandard(
            lambda self, a: 0.5,
            "indifferent"
        )

    @staticmethod
    def LINEAR_HIGHER_THE_BETTER():
        return AttractivenessStandard(
            lambda self, a: a,
            "linear higher the better"
        )

    @staticmethod
    def SIMILAR_THE_BETTER():
        return AttractivenessStandard(
            lambda self, a: U.sigmoid(a,
                                      mid_point=self.physical_attrs.attractiveness,
                                      rate=0.1),
            "similar the better"
        )

    @staticmethod
    def HIGH_STANDARD():
        return AttractivenessStandard(
            lambda self, a: U.sigmoid(a,
                                      mid_point=0.7,
                                      rate=0.08),
            "high standard"
        )


class HeightStandard(Standard):
    '''
    has a score_fn field
    which is a function that takes in height
        and returns a score between 0 and 1
    '''

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
                HeightStandard.LOWER_THE_BETTER(),
                HeightStandard.MUST_BELOW_HEIGHT(),
                HeightStandard.HIGHER_THE_BETTER(),
            ]
            weights = [0.2, 0.4, 0.2, 0.2]

        elif gender == 'Female':
            stds = [
                HeightStandard.NO_HEIGHT_STANDARD(),
                HeightStandard.HIGHER_THE_BETTER(),
                HeightStandard.MUST_ABOVE_HEIGHT(),
                HeightStandard.LOWER_THE_BETTER(),
            ]
            weights = [0.2, 0.4, 0.2, 0.2]
        else:
            stds = [
                HeightStandard.NO_HEIGHT_STANDARD(),
                HeightStandard.HIGHER_THE_BETTER(),
                HeightStandard.LOWER_THE_BETTER(),
                HeightStandard.MUST_BELOW_HEIGHT(),
                HeightStandard.MUST_ABOVE_HEIGHT(),
            ]
            weights = [0.2, 0.2, 0.2, 0.2, 0.2]

        std = random.choices(stds, weights=weights)
        return std[0]

    # region some common default hard standards
    @staticmethod
    def HIGHER_THE_BETTER(half_score_height=None, rate=8):
        '''
        half_score_height is the height that can achieve 0.5
        '''

        def fn(self, height, half_score_height=half_score_height, rate=rate):
            if half_score_height == None:
                half_score_height = self.physical_attrs.height
            # return height / (height + half_score_height)
            return U.sigmoid(height, mid_point=half_score_height, rate=rate)

        return HeightStandard(fn, "higher the better")

    @staticmethod
    def LOWER_THE_BETTER(half_score_height=None):
        '''
        half_score_height is the height that can achieve 0.5
        '''

        def fn(self, height, half_score_height=half_score_height):
            if half_score_height == None:
                half_score_height = self.physical_attrs.height
            h = max(2 * half_score_height - height, 0)
            # return h / (h + half_score_height)
            return U.sigmoid(h, mid_point=half_score_height, rate=8)

        return HeightStandard(fn, "lower the better")

    @staticmethod
    def MUST_ABOVE_HEIGHT(min_height=None):
        '''
        if no min_height given
        assume it is above person's own height
        '''

        def fn(self, height, min_height=min_height):
            if min_height == None:
                min_height = self.physical_attrs.height
            return int(height >= min_height)

        std_name = f"must above own height" if min_height == None \
            else f"must above {min_height:2f} cm"
        return HeightStandard(fn, std_name)

    @staticmethod
    def MUST_BELOW_HEIGHT(max_height=None):
        def fn(self, height, max_height=max_height):
            if max_height == None:
                max_height = self.physical_attrs.height
            return int(height <= max_height)

        std_name = f"must below own height" if max_height == None \
            else f"must below {max_height:2f} cm"
        return HeightStandard(fn, std_name)

    @staticmethod
    def MUST_BETWEEN_HEIGHT(min_height=None, max_height=None):
        def fn(height): return int(height >= min_height
                                   and height <= max_height)
        return HeightStandard(fn, f"must between {min_height} and {max_height} cm")

    @staticmethod
    def NO_HEIGHT_STANDARD():
        def fn(self, height): return 0.5
        return HeightStandard(fn, "indifferent")
    # endregion


class AgeStandard(Standard):

    @staticmethod
    def get_random_age_std(basic_attrs: BasicAttributes):
        gender = basic_attrs.gender
        if gender == 'Male':
            stds = [
                AgeStandard.NO_AGE_STANDARD(),
                AgeStandard.MUST_ABOVE_AGE(),
                AgeStandard.MUST_BELOW_AGE()
            ]
            weights = [0.5, 0.1, 0.4]

        elif gender == 'Female':
            stds = [
                AgeStandard.NO_AGE_STANDARD(),
                AgeStandard.MUST_ABOVE_AGE(),
                AgeStandard.MUST_BELOW_AGE()
            ]
            weights = [0.5, 0.4, 0.1]
        else:
            stds = [
                AgeStandard.NO_AGE_STANDARD(),
                AgeStandard.MUST_ABOVE_AGE(),
                AgeStandard.MUST_BELOW_AGE()
            ]
            weights = [0.6, 0.2, 0.2]

        std = random.choices(stds, weights=weights)
        return std[0]

    # Factory Methods

    @staticmethod
    def NO_AGE_STANDARD():
        return AgeStandard(
            lambda p, age: 0.5,
            "indifferent"
        )

    @staticmethod
    def MUST_ABOVE_AGE(min_age=None):
        '''
        min age: in years
        if no min_age given
        assume it is above person's own age
        '''

        def fn(self, age, min_age=min_age):
            if min_age == None:
                min_age = self.basic_attrs.get_age_in_years()
            return int(age >= min_age)

        std_name = f"must above own age" if min_age == None \
            else f"must above {min_age:2f} years old"
        return AgeStandard(fn, std_name)

    @staticmethod
    def MUST_BELOW_AGE(max_age=None):
        '''
        max age: in years
        if no max_age given
        assume it is above person's own age
        '''

        def fn(self, age, max_age=max_age):
            if max_age == None:
                max_age = self.basic_attrs.get_age_in_years()
            return int(age <= max_age)

        std_name = f"must below own age" if max_age == None \
            else f"must below {max_age:2f} years old"
        return AgeStandard(fn, std_name)


class PartnerStandards:
    def __init__(
            self,
            height_std: HeightStandard,
            age_std: AgeStandard,
            attractive_std: AttractivenessStandard) -> None:

        self.height_std = height_std
        self.age_std = age_std
        self.attractive_std = attractive_std

    def score(self, my_person, candidate) -> float:
        '''
        calculate a score of the candidate
        base on various standards
        '''
        height_score = self.height_std.score_fn(
            my_person,
            candidate.physical_attrs.height
        )
        age_score = self.age_std.score_fn(
            my_person,
            candidate.basic_attrs.age
        )
        attractiveness_score = self.attractive_std.score_fn(
            my_person,
            candidate.physical_attrs.attractiveness
        )
        # TODO: finish score fn, with weights
        scores = [height_score, age_score, attractiveness_score]
        weights = [1, 1, 1]
        return U.weighted_sum(scores, weights)

    @staticmethod
    def generate_random_partner_standards(
            basic_attrs: BasicAttributes,
            physical_attrs: PhysicalAttributes):
        height_std = HeightStandard.get_random_height_std(
            basic_attrs, physical_attrs)
        age_std = AgeStandard.get_random_age_std(basic_attrs)
        attractive_std = AttractivenessStandard.generate_random_std()
        return PartnerStandards(height_std, age_std, attractive_std)
