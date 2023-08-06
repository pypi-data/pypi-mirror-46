from re import match
from decimal import Decimal, InvalidOperation




def get_decimal(value):
    '''
    Returns the decimal segment of a number (value after the decimal) as a string
    '''
    return str(value).split('.')[1]


def is_whole(value):
    '''
    Returns True if value is a whole number (has no decimal places)
    Value may be an integer or a string integer
    https://stackoverflow.com/a/6239987
    '''
    try:
        return float(value).is_integer()
    except (ValueError, TypeError, InvalidOperation):
        return False


def is_decimal(value):
    '''
    Returns true if the argument is a valid Decimal value
    '''
    try:
        Decimal(value)
        return True
    except (ValueError, TypeError, InvalidOperation):
        return False


def get_percent(numerator, denominator):
    '''
    Generates the percentage of the numerator over the denominator
    '''
    return numerator / denominator * 100


def is_convertable_to_int(value):
    '''
    Returns True if value can be converted to an int, otherwise False
    '''
    try:
        int(value)
        return True
    except (ValueError, TypeError, InvalidOperation):
        return False


def is_int(value):
    '''
    Returns True if argument is of integer type, otherwise False
    '''
    return isinstance(value, int)


def is_valid_latitude(value):
    '''
    Returns True if the supplied value is a valid latitude (between -90 [southern hemisphere] and +90 [northern hemisphere])
    Value may be of string or number type
    Based on regex from https://stackoverflow.com/a/18690202
    '''
    return match(r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$', str(value)) is not None


def is_valid_longitude(value):
    '''
    Returns True if the supplied value is a valid longitude (between -180 [east] and +180 [west])
    Value may be of string or number type
    Based on regex from https://stackoverflow.com/a/18690202
    '''
    return match(r'^[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$', str(value)) is not None


def is_positive(value):
    '''
    Returns True is the value is a positive number
    '''
    return value > 0


def is_negative(value):
    '''
    Returns True is the value is a negative number
    '''
    return value < 0
