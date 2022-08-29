import random
from attributes import *
from standards import PartnerStandards
from typing import *
import attr_funcs as F


class Person:
    def __init__(
            self,
            basic_attrs: BasicAttributes,
            physical_attrs: PhysicalAttributes,
            mental_attrs: MentalAttributes,
            partner_stds: PartnerStandards,
            alive=True,
            acquaintances=[],
            partner=None) -> None:

        self.basic_attrs = basic_attrs
        self.physical_attrs = physical_attrs
        self.mental_attrs = mental_attrs
        self.partner_stds = partner_stds
        self.alive = alive
        self.aquaintances = acquaintances
        self.partner = partner

        # generate unique id
        self.id = F.get_unique_id(self.basic_attrs)

    def is_Male(self):
        return self.basic_attrs.gender == 'Male'

    def is_Female(self):
        return self.basic_attrs.gender == 'Female'

    @staticmethod
    def generate_random_person(age_bounds: Tuple[int, int] = (0, 1)):
        basic_attrs = BasicAttributes.get_random_attributes(age_bounds)
        physical_attrs = PhysicalAttributes.get_random_attributes(basic_attrs)
        mental_attrs = MentalAttributes.get_random_attributes()
        partner_stds = PartnerStandards.generate_random_partner_standards(
            basic_attrs, physical_attrs)
        return Person(basic_attrs, physical_attrs, mental_attrs, partner_stds)

    def get_description(self, detail_level='basic', bounds=True):
        desp = (
            f"uid: {self.id} \n"
            f"alive: {self.alive} \n"
            f"name: {self.basic_attrs.given_name} \n"
            f"age: {self.basic_attrs.get_age_in_years()} years old\n"
            f"gender: {self.basic_attrs.gender}"
        )
        mental_desp = (
            "\n === Mental Attrs === \n"
            f"social level: {self.mental_attrs.social_level:.2f}"
        )
        physical_desp = (
            "\n === Physical Attrs === \n"
            f"height: {self.physical_attrs.height:.2f} cm \n"
            f"attractiveness: {self.physical_attrs.attractiveness:.2f}"
        )
        stds = (
            "\n === Partner Standards === \n"
            f"height standard: {self.partner_stds.height_std.std_name}\n"
            f"age standard: {self.partner_stds.age_std.std_name}"
        )
        detail_levels = {
            'basic': desp,
            'detailed': desp + mental_desp + physical_desp,
            'full': desp + mental_desp + physical_desp + stds,
        }
        desp = detail_levels[detail_level]
        if bounds:
            desp = "-"*30 + '\n' + desp + '\n' + '-'*30
        return desp

    def grow_old(self) -> bool:
        self.basic_attrs.age += 1
        dead_by_old_age = self.natural_death()
        self.alive = not dead_by_old_age
        return dead_by_old_age

    def natural_death(self):
        mort_rate = F.get_mortality_rate(self.basic_attrs)
        if random.random() < mort_rate:
            # natural death
            death_msg = f"{self.basic_attrs.given_name} has died "\
                f"at age {self.basic_attrs.get_age_in_years()}"\
                f", cause: natural death"
            print(death_msg)
            return True
        else:
            return False

    def socialize(self, people: List):
        '''
        choose who to socialise with, base on social_level
        give acquaintances scores
        attempt to propose to the one with highest score
        '''
        num_ppl_socialize = F.get_num_ppl_to_socialize(self.mental_attrs)
        known_ppl = random.sample(people, num_ppl_socialize)[
            :num_ppl_socialize]
        if self in known_ppl:
            num_ppl_socialize -= 1
            known_ppl.remove(self)
        print(
            f"{self.id} decides to socialize with {num_ppl_socialize} people:\n {[p.id for p in known_ppl]}")
        return num_ppl_socialize
