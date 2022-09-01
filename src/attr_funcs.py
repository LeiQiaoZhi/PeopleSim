import random
import uuid
from attributes import *
import utils.util_funcs as U


def get_unique_id(basic_attrs: BasicAttributes, mental_attrs: MentalAttributes):
    gender_to_id = {
        'Male': 'M',
        'Female': 'F',
        'Others': 'O'
    }
    uid = [gender_to_id.get(basic_attrs.gender),
           basic_attrs.given_name,
           basic_attrs.surname,
           'I' if mental_attrs.social_level < 0.5 else 'E',
           str(uuid.uuid1())]
    return '-'.join(uid)


def get_mortality_rate(basic_attrs: BasicAttributes, base=0.001):
    '''
    Returns:
    the chance of natural death of a person

    base on age (in years)
    ideas: gender, health

    function:
        f\left(x\right)=\frac{1}{1+e^{-\frac{x-100}{10}}}
    '''
    age = basic_attrs.get_age_in_years()
    return U.sigmoid(age,
                     mid_point=100,
                     rate=10)


def get_num_ppl_to_socialize(mental_attrs: MentalAttributes):
    '''
    return the number of people a person choose to socialize with
    base on the person's social level
    '''
    social_level = mental_attrs.social_level
    return max(0, round(random.normalvariate(social_level*5, 1)))
