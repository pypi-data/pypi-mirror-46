import string
import random




def get_random_string(length, chars=string.digits + string.punctuation + string.ascii_letters + string.hexdigits + string.octdigits):
    '''
    Returns a random string consisting of characters supplied and of length specified
    '''
    return ''.join(random.choice(chars) for _ in range(length))


def get_random_sha1():
    '''
    Returns a random SHA1 value
    '''
    return get_random_string(40, string.hexdigits.lower())
    

def randomize_case(str):
    '''
    Returns the supplied string with each character's case randomized
    '''
    lower = str.lower()
    upper = str.upper()
    return ''.join(x[random.randint(0,1)] for x in zip(lower, upper))
