import random
import math
from typing import Tuple
import os
import sys


class BasicAttributes:
    '''
    given name
    surname
    age:  is in terms of months
    gender: Male, Female, Others
    '''

    def __init__(
            self,
            given_name: str,
            surname: str,
            age: int,
            gender: str) -> None:
        self.given_name = given_name
        self.surname = surname
        self.age = age
        self.gender = gender

    @staticmethod
    def get_random_attributes(age_bounds: Tuple[int, int] = (0, 1)):
        gender = BasicAttributes._get_random_gender()
        name = BasicAttributes._get_random_name(gender)
        surname = BasicAttributes._get_random_surname()
        return BasicAttributes(
            given_name=name,
            surname=surname,
            age=random.randrange(*age_bounds),
            gender=gender
        )

    @staticmethod
    def _get_random_gender():
        genders = ['Male', 'Female', 'Others']
        weights = [0.4, 0.4, 0.2]
        return random.choices(genders,weights=weights)[0]

    @staticmethod
    def _get_random_name(gender):
        # read names from data
        current_dir = os.path.dirname(os.path.realpath(__file__))
        female_path = os.path.join(current_dir, "data", "female_names.txt")
        with open(female_path) as f:
            female_names = f.read().split('\n')
        male_path = os.path.join(current_dir, "data", "male_names.txt")
        with open(male_path) as f:
            male_names = f.read().split('\n')

        # random choice of name
        if gender == 'Male':
            return random.choice(male_names)
        elif gender == 'Female':
            return random.choice(female_names)
        else:
            return random.choice(male_names+female_names)

    def _get_random_surname():
        current_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(current_dir, "data", "male_names.txt")
        with open(path) as f:
            surnames = f.read().split('\n')
        return random.choice(surnames)

    def get_age_in_years(self, exact=False):
        if exact:
            return self.age / 12
        return self.age // 12


class PhysicalAttributes:
    '''
    height: in terms of cm
    attractiveness: normally 0-1, mean 0.5, std 0.2
    '''
    mean_male_height = 175
    mean_female_height = 165

    def __init__(self, height, attractiveness) -> None:
        self.height = height
        self.attractiveness = attractiveness

    @staticmethod
    def get_random_attributes(basic_attr: BasicAttributes):
        height = PhysicalAttributes._get_random_height(basic_attr.gender)
        attractiveness = PhysicalAttributes._get_random_attractiveness()
        return PhysicalAttributes(height, attractiveness)

    @staticmethod
    def _get_random_height(gender):
        if gender == 'Male':
            mean, std = PhysicalAttributes.mean_male_height, 10
        else:
            mean, std = PhysicalAttributes.mean_female_height, 10
        return random.normalvariate(mean, std)

    @staticmethod
    def _get_random_attractiveness():
        return random.normalvariate(0.5, 0.2)


class MentalAttributes:
    '''
    social level: from 0 to 1
    '''

    def __init__(self, social_level):
        self.social_level = social_level

    @staticmethod
    def get_random_attributes():
        social_level = MentalAttributes._get_random_social_level()
        return MentalAttributes(social_level)

    @staticmethod
    def _get_random_social_level():
        social_level = random.normalvariate(0.5, 0.3)
        return min(max(social_level, 0), 1)
