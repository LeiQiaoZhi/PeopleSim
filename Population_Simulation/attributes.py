import random
import math

class BasicAttributes:
    '''
    given name
    age:  is in terms of months
    gender: Male, Female, Others
    '''

    def __init__(self, given_name, age, gender) -> None:
        self.given_name = given_name
        self.age = age
        self.gender = gender

    @staticmethod
    def get_random_attributes():
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


class PhysicalAttributes:
    '''
    height: in terms of cm
    attractiveness: normally 0-1, mean 0.5, std 0.2
    '''
    def __init__(self, height, attractiveness) -> None:
        self.height = height
        self.attractiveness = attractiveness

    @staticmethod
    def get_random_attributes(basic_attr: BasicAttributes):
        height = PhysicalAttributes._get_random_height(basic_attr.gender)
        attractiveness = PhysicalAttributes._get_random_attractiveness()
        return PhysicalAttributes(height,attractiveness)

    @staticmethod
    def _get_random_height(gender):
        if gender == 'Male':
            mean, std = 175, 10
        else:
            mean, std = 165, 10
        return random.normalvariate(mean, std)

    @staticmethod
    def _get_random_attractiveness():
        return random.normalvariate(0.5,0.2)


class MentalAttributes:
    def __init__(self, social_level):
        self.social_level = social_level

    @staticmethod
    def get_random_attributes():
        social_level = MentalAttributes._get_random_social_level()
        return MentalAttributes(social_level)

    @staticmethod
    def _get_random_social_level():
        social_level = random.normalvariate(0.5,0.3)
        return min(max(social_level,0),1)