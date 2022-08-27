import random

from typing import *
from attr_funcs import *


class BasicAttributes:
    '''
    age:  is in terms of months
    '''

    def __init__(self, given_name, age, gender) -> None:
        self.given_name = given_name
        self.age = age
        self.gender = gender

    @staticmethod
    def get_random_basic_attributes():
        gender = BasicAttributes._get_random_gender()
        name = BasicAttributes._get_random_name(gender)
        return BasicAttributes(
            given_name=name,
            age=0,
            gender=gender
        )

    @staticmethod
    def _get_random_gender():
        genders = ['Male', 'Female', 'Others']
        return random.choice(genders)

    @staticmethod
    def _get_random_name(gender):
        male_names = ['Albert', 'Bob', 'Calvin', 'Kevin']
        female_names = ['Alice', 'Cath', 'Debula', 'Karen']
        if gender == 'Male':
            return random.choice(male_names)
        elif gender == 'Female':
            return random.choice(female_names)
        else:
            return random.choice(male_names+female_names)

    def get_age_in_years(self, exact=False):
        if exact:
            return self.age / 12
        return self.age // 12


class Person:
    def __init__(self, basic_attrs: BasicAttributes) -> None:
        self.basic_attrs = basic_attrs

    def get_basic_description(self, bounds=True):
        desp = (
            f"name: {self.basic_attrs.given_name} \n"
            f"age: {self.basic_attrs.get_age_in_years()}\n"
            f"gender: {self.basic_attrs.gender}"
        )
        if bounds:
            desp = "-"*30 + '\n' + desp + '\n' + '-'*30
        return desp

    def grow_old(self) -> bool:
        self.basic_attrs.age += 1
        dead_by_old_age = self.natural_death()
        return dead_by_old_age

    def natural_death(self):
        mort_rate = get_mortality_rate(self)
        if random.random() < mort_rate:
            # natural death
            death_msg = f"{self.basic_attrs.given_name} has died "\
                f"at age {self.basic_attrs.get_age_in_years()}"\
                f", cause: natural death"
            print(death_msg)
            return True
        else:
            return False
