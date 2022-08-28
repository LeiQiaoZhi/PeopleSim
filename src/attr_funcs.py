import random
import uuid
from attributes import *

def get_unique_id(basic_attrs: BasicAttributes):
    gender_to_id = {
        'Male': 'M',
        'Female': 'F',
        'Others': 'O'
    }
    uid = [gender_to_id[basic_attrs.gender] 
        , basic_attrs.given_name 
        , str(uuid.uuid1())]
    return '-'.join(uid)

def get_mortality_rate(basic_attrs, base=0.001):
    '''
    return the chance of natural death of a person

    base on age 
    ideas: gender, health
    '''
    # TODO: use a mortality function based on age
    return base


def get_num_ppl_to_socialize(mental_attrs: MentalAttributes):
    '''
    return the number of people a person choose to socialize with
    base on the person's social level
    '''
    social_level = mental_attrs.social_level
    return max(0, round(random.normalvariate(social_level*5,1)))