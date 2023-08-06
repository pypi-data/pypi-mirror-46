import random




def get_random_decimal(low, high, max_decimal_places):
    '''
    Returns a random decimal number between values specified (inclusive of values specified)
    https://docs.python.org/3/library/random.html#random.uniform
    '''
    return round(random.uniform(low, high), max_decimal_places)


def get_random_latitude(max_decimal_places=8):
    '''
    Returns a random valid latitude value (between -90 [southern hemisphere] and +90 [northern hemisphere])
    '''
    return get_random_decimal(-90, 90, max_decimal_places)


def get_random_longitude(max_decimal_places=8):
    '''
    Returns a random valid longitude value (between -180 [east] and +180 [west])
    '''
    return get_random_decimal(-180, 180, max_decimal_places)
