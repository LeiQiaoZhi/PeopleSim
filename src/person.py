import random
from attributes import *
from standards import PartnerStandards
from typing import *
import attr_funcs as F
import utils.util_funcs as U
from utils.logger import Logger


class Person:
    def __init__(
            self,
            basic_attrs: BasicAttributes,
            physical_attrs: PhysicalAttributes,
            mental_attrs: MentalAttributes,
            partner_stds: PartnerStandards,
            alive=True,
            partner=None) -> None:

        self.basic_attrs = basic_attrs
        self.physical_attrs = physical_attrs
        self.mental_attrs = mental_attrs
        self.partner_stds = partner_stds
        self.alive = alive
        self.partner = partner

        # non-param fields
        self.acquaintances: Dict[str, float] = dict()
        self.target = None

        # generate unique id
        self.id = F.get_unique_id(self.basic_attrs, self.mental_attrs)

    ### Getters ###
    def is_equal(self, person):
        if person == None:
            return False
        return self.id == person.id

    def is_alive(self):
        return self.alive

    def is_male(self):
        return self.basic_attrs.gender == 'Male'

    def is_female(self):
        return self.basic_attrs.gender == 'Female'

    def get_pronoun(self):
        pronoun_dict = {
            'Male': 'he',
            'Female': 'she',
            'Others': 'they'
        }
        return pronoun_dict[self.basic_attrs.gender]

    def get_full_name(self):
        return f"{self.basic_attrs.given_name} {self.basic_attrs.surname}"

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
            f'{Logger.divider()}\n'
            f"{Logger.yellow(self.get_full_name())} "
            f"with social level {self.mental_attrs.social_level:.2f} "
            f"decides to socialize with {num_ppl_socialize} people:"
            f"\n {[p.get_full_name() for p in known_ppl]}"
            f"\n scores: {scores}"
            f"\n aquaintances: {len(self.acquaintances)}"
            f"\n age: {self.partner_stds.age_std.std_name} height: {self.partner_stds.height_std.std_name}"
        )

        return num_ppl_socialize, len(self.acquaintances)

    def rank_acquaintances(self, people):
        if len(self.acquaintances) == 0:
            print(f"\n{self.get_full_name()} is lonely."
                  f"{self.get_pronoun()} choose to socialize with no one.")
            return

        # rank acquantances by scores
        ranked = sorted(self.acquaintances.items(), key=lambda x: x[1],
                        reverse=True)

        target_id, score = ranked[0]
        target: Person = U.find_person_by_id(people, target_id)
        self.target = target
        print(
            f"{Logger.yellow(self.get_full_name())}'s target is {Logger.cyan(target.get_full_name())}, with a score of {score:.2f}.")

    def find_match(self) -> bool:
        if self.target == None:
            print(f"{Logger.bold(self.get_full_name())} has no target.")
            return False
        if self.is_equal(self.target.target):
            Logger.print_title("Match found!")
            print(f"{Logger.yellow(self.get_full_name())} forms a match with "
                  f"{Logger.cyan(self.target.get_full_name())}")
            return True
        print(f"No match found :(")
        return False
