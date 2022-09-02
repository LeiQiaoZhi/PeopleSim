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

    # TODO get other types of pronoun his her

    def get_full_name(self):
        return f"{self.basic_attrs.given_name} {self.basic_attrs.surname}"

    def partner_score(self, candidate) -> float:
        return self.partner_stds.score(self, candidate)

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
            f"name: {Logger.yellow(self.get_full_name())} \n"
            f"age: {self.basic_attrs.get_age_in_years()} years old\n"
            f"gender: {self.basic_attrs.gender}"
        )
        mental_desp = (
            f"{Logger.title('Mental Attrs',char='=',length=3)}"
            f"social level: {self.mental_attrs.social_level:.2f}"
        )
        physical_desp = (
            f"{Logger.title('Physical Attrs',char='=',length=3)}"
            f"height: {self.physical_attrs.height:.2f} cm \n"
            f"attractiveness: {self.physical_attrs.attractiveness:.2f}"
        )
        stds = (
            f"{Logger.title('Partner Standards',char='=',length=3)}"
            f"height standard: {self.partner_stds.height_std.std_name}\n"
            f"age standard: {self.partner_stds.age_std.std_name} \n"
            f"attractiveness standard: {self.partner_stds.attractive_std.std_name}"
        )
        detail_levels = {
            'basic': desp,
            'detailed': desp + mental_desp + physical_desp,
            'full': '\n'.join([desp, mental_desp, physical_desp, stds]),
        }
        desp = detail_levels[detail_level]
        if bounds:
            desp = "="*30 + '\n' + desp + '\n' + '='*30
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
            Logger.important(death_msg, color=Logger.DARKCYAN)
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
        scores = [self.partner_score(p) for p in known_ppl]

        # add known_ppl to aquaintances
        for p, score in zip(known_ppl, scores):
            self.acquaintances[p.id] = score

            # add self to others
            self_score = p.partner_score(self)
            p.acquaintances[self.id] = self_score

        Logger.info(
            f'{Logger.divider()}\n'
            f"{Logger.yellow(self.get_full_name())} "
            f"with social level {self.mental_attrs.social_level:.2f} "
            f"decides to socialize with {num_ppl_socialize} people:"
            f"\n {[p.get_full_name() for p in known_ppl]}"
            f"\n scores: {scores}"
            f"\n aquaintances: {len(self.acquaintances)}"
            f"\n age: {self.partner_stds.age_std.std_name} |"
            f"height: {self.partner_stds.height_std.std_name} |"
            f"attrnss: {self.partner_stds.attractive_std.std_name}"
        )

        return num_ppl_socialize, len(self.acquaintances)

    def rank_acquaintances(self, people):
        if len(self.acquaintances) == 0:
            Logger.info(f"\n{self.get_full_name()} is lonely."
                        f"{self.get_pronoun()} choose to socialize with no one.")
            return

        # rank acquantances by scores
        ranked = sorted(self.acquaintances.items(), key=lambda x: x[1],
                        reverse=True)

        target_id, score = ranked[0]
        target: Person = U.find_person_by_id(people, target_id)
        if target == None:
            Logger.warn(f"cannot find person with id{target_id}")
            return
        self.target = target
        Logger.info(
            f"{Logger.yellow(self.get_full_name())}'s target is "
            f"{Logger.cyan(target.get_full_name())}, "
            f"with a score of {score:.2f}.")

    def find_match(self) -> bool:
        match_result = {"result": "", "target target": None,
                        "target target score": None, "self score": None}
        if self.target == None:
            Logger.info(f"{Logger.bold(self.get_full_name())} has no target.")
            match_result['result'] = "No target"
            return False, match_result
        if self.is_equal(self.target.target):
            Logger.info(Logger.bold("<Match found>"))
            Logger.info(f"{Logger.yellow(self.get_full_name())} forms a match with "
                        f"{Logger.cyan(self.target.get_full_name())}")
            match_result['result'] = "Match found"
            return True, match_result
        elif self.target.target == None:
            # shouldn't really happen
            Logger.warn("Target is none")
            Logger.warn(f"{self.target.acquaintances}")
            return False, match_result

        Logger.info(
            f"No match found for {Logger.yellow(self.get_full_name())} :(")

        Logger.info(f"{Logger.cyan(self.target.get_full_name())}'s target is "
                    f"{Logger.purple(self.target.target.get_full_name())} "
                    f"with a score of {Logger.bold(f'{self.target.partner_score(self.target.target):.2f}')}, "
                    f"while your score is {Logger.bold(f'{self.target.partner_score(self):.2f}')}")

        match_result = {
            "result": "",
            "target target": self.target.target.get_full_name(),
            "target target score": round(self.target.partner_score(self.target.target), 2),
            "self score": round(self.target.partner_score(self), 2)
        }
        match_result['result'] = "No match"
        return False, match_result

    def post_social(self):
        '''
        called after each social step,
        some acquantances fade away from life,
        for now, just hard reset
        '''
        self.acquaintances = {}
        self.target = None
