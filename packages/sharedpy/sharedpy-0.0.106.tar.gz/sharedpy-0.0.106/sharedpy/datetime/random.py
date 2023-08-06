import datetime
from random import randrange
from datetime import timedelta




def random_datetime(start, end):
    '''
    Returns a random datetime between two datetime objects.
    https://stackoverflow.com/a/553448/1095373
    '''
    delta = end - start
    total_delta_seconds = (delta.days * 24 * 60 * 60) + delta.seconds
    random_seconds_within_delta = randrange(0, total_delta_seconds)
    return start + timedelta(seconds=random_seconds_within_delta)


def get_random_datetime_in_past():
    """
    Returns a random datetime between two datetime objects.
    """
    return random_datetime(datetime.datetime.min, datetime.datetime.now())
