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
            # acquaintances: Dict[str, float],
            partner=None) -> None:

        self.basic_attrs = basic_attrs
        self.physical_attrs = physical_attrs
        self.mental_attrs = mental_attrs
        self.partner_stds = partner_stds
        self.alive = alive
        self.acquaintances: Dict[str, float] = dict()
        self.partner = partner

        # generate unique id
        self.id = F.get_unique_id(self.basic_attrs, self.mental_attrs)

    ### Getters ###
    def is_alive(self):
        return self.alive

    def is_male(self):
        return self.basic_attrs.gender == 'Male'

    def is_female(self):
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
            f"name: {self.basic_attrs.given_name} {self.basic_attrs.surname} \n"
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
        '''
        num_ppl_socialize = F.get_num_ppl_to_socialize(self.mental_attrs)
        known_ppl: List[Person] = random.sample(people, num_ppl_socialize)[
            :num_ppl_socialize]
        if self in known_ppl:
            num_ppl_socialize -= 1
            known_ppl.remove(self)
        scores = [self.partner_stds.score(self, p) for p in known_ppl]

        # add known_ppl to aquaintances
        for p, score in zip(known_ppl, scores):
            self.acquaintances[p.id] = score

            # add self to others
            self_score = p.partner_stds.score(p, self)
            p.acquaintances[self.id] = self_score

        print(
            f'{"="*50}\n'
            f"{self.basic_attrs.given_name + ' ' + self.basic_attrs.surname} "
            f"with social level {self.mental_attrs.social_level:.2f} "
            f"decides to socialize with {num_ppl_socialize} people:"
            f"\n {[p.basic_attrs.given_name + ' ' + p.basic_attrs.surname for p in known_ppl]}"
            f"\n scores: {scores}"
            f"\n aquaintances: {len(self.acquaintances)}"
            f"\n age: {self.partner_stds.age_std.std_name} height: {self.partner_stds.height_std.std_name}"
        )
        return num_ppl_socialize, len(self.acquaintances)
