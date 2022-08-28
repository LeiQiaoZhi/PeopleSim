import random
from attributes import *
from typing import *
from attr_funcs import *


class Person:
    def __init__(
            self,
            basic_attrs: BasicAttributes,
            physical_attrs: PhysicalAttributes,
            alive = True,
            acquaintances = [],
            partner = None ) -> None:
           
        self.basic_attrs = basic_attrs
        self.physical_attrs = physical_attrs
        self.alive = alive
        self.aquaintances = acquaintances
        self.partner = partner

    @staticmethod
    def generate_random_person():
        basic_attrs = BasicAttributes.get_random_attributes()
        physical_attrs = PhysicalAttributes.get_random_attributes(basic_attrs)
        return Person(basic_attrs,physical_attrs)

    def get_description(self, detail_level='basic', bounds=True):
        desp = (
            f"name: {self.basic_attrs.given_name} \n"
            f"age: {self.basic_attrs.get_age_in_years()}\n"
            f"gender: {self.basic_attrs.gender}"
        )
        if detail_level == 'detailed':
            # TODO: add detailed description
            desp += ""
        if bounds:
            desp = "-"*30 + '\n' + desp + '\n' + '-'*30
        return desp

    def grow_old(self) -> bool:
        self.basic_attrs.age += 1
        dead_by_old_age = self.natural_death()
        self.alive = not dead_by_old_age
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

    def socialize(self):
        '''
        choose who to socialise with, base on social_level
        give acquaintances scores
        attempt to propose to the one with highest score
        '''
        pass