import random
from random import randrange

from .utils import is_iterable




def get_random_index(iterable):
    '''
    Returns a random index number from within the iterable argument
    '''
    return randrange(len(iterable))


def get_random_item(iterable):
    '''
    Returns a random item selected from the iterable
    '''
    return random.sample(iterable, 1)[0]


def shuffle_iterable(iterable):
    '''
    Randomly shuffles the supplied iterable
    Note: Does not support dictionaries
    http://stackoverflow.com/questions/12073425/how-to-mix-queryset-results
    '''
    return sorted(iterable, key=lambda x: random.random())
