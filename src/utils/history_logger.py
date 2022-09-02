from typing import *
from utils.logger import Logger
from attributes import *
from person import Person


class History:
    def __init__(self, person: Person) -> None:
        self.person = person
        self.original_age = person.basic_attrs.age  # in months
        self.death = {"cause": ""}
        self.social_history = {'num_socials': [],
                               'acquaintances': [], 'targets': [], 'match_result': []}

    def get_age_in_years(self, step, exact=False):
        age = self.original_age + step
        age = round(age / 12, 2) if exact else age//12
        return age

    def log_social_history(self, num_social, acquaintances):
        self.social_history['acquaintances'].append(acquaintances)
        self.social_history['num_socials'].append(num_social)

    def log_partner_target(self, target):
        self.social_history['targets'].append(target)

    def log_match_result(self, match_result):
        self.social_history['match_result'].append(match_result)

    def get_success_match_num(self):
        success = filter(
            lambda result: result['result'] == 'Match found', self.social_history['match_result'])
        return len(list(success))

    def to_string(self, detail_level='summary') -> str:
        title = Logger.title(
            f"History of {Logger.yellow(self.person.get_full_name())}", char='=', total_length=70)
        description = self.person.get_description(
            detail_level='full', bounds=False)

        full_social_msgs = []
        for step in range(len(self.social_history['num_socials'])):
            acq = self.social_history['acquaintances'][step]
            target = self.social_history['targets'][step]
            num_social = self.social_history['num_socials'][step]
            match_result = self.social_history['match_result'][step]

            step_msg = f"Step {step}"
            social_msg = (f'{Logger.title(step_msg,char="-",length=3)}'
                          f"At the age of {self.get_age_in_years(step,exact=True)},\n"
                          f"{Logger.yellow(self.person.get_full_name())} "
                          f"with social level {self.person.mental_attrs.social_level:.2f} "
                          f"decides to socialize with {Logger.bold(num_social)} people, "
                          f"and made {Logger.bold(len(acq))} aquaintances."
                          f"\n{self.person.get_pronoun(belong=True)} target is {Logger.cyan(target) if target != None else 'None'}"
                          )

            result_msg_dict = {
                'No match':
                    (f"{Logger.cyan(target)}'s target is "
                     f"{Logger.purple(match_result['target target'])} "
                     f"with a score of {Logger.bold(match_result['target target score'])}, "
                     f"while your score is {Logger.bold(match_result['self score'])}"),
                'Match found':
                    (f"{Logger.cyan(target)}'s target is {Logger.yellow(self.person.get_full_name())}"
                     f"\n{Logger.bold('Match made!')}"),
                'No target':
                    f"No target :("
            }

            # print(match_result)
            full_social_msgs.append(
                social_msg + '\n' + result_msg_dict[match_result['result']])

        if self.person.is_alive():
            death_msg = "Still alive"
        else:
            death_msg = f"{self.person.basic_attrs.given_name} has died "\
                f"at age {self.person.basic_attrs.get_age_in_years()}"\
                f", cause: {self.death['cause']}"

        social_summary = Logger.title("Social Summary", char='-', length=3) + \
            Logger.bold(
            f"In total, {self.person.get_pronoun()} has {Logger.blue(self.get_success_match_num())} successful matches")
        social_history_dict = {
            'full':
                Logger.title("Social History", char='=') +
                '\n'.join(full_social_msgs) + '\n' + social_summary, 'summary': social_summary}
        death_msg = Logger.title("Status", char='=') + \
            Logger.blue(death_msg)
        end = Logger.title(
            f"End of history of {Logger.yellow(self.person.get_full_name())}", char='=', total_length=70)

        msg = [
            title,
            description,
            social_history_dict[detail_level],
            death_msg,
            end
        ]
        return '\n'.join(msg)


class HistoryLogger:
    def __init__(self) -> None:
        self.history_dict: Dict[str, History] = {}

    def init_history(self, person):
        '''
        called to init history for a person
        '''
        self.history_dict[person.id] = History(person)

    def print_history(self, person_id):
        print(self.history_dict[person_id].to_string())

    def log_death(self, person, cause):
        self.history_dict[person.id].death['cause'] = cause

    def log_socialize_history(self, person, num_ppl_socialize):
        self.history_dict[person.id].log_social_history(
            num_social=num_ppl_socialize,
            acquaintances=person.acquaintances,
        )

    def log_partner_target(self, person):
        self.history_dict[person.id].log_partner_target(
            person.target.get_full_name() if person.target != None else "None")

    def log_match_result(self, person, match_result):
        self.history_dict[person.id].log_match_result(match_result)
