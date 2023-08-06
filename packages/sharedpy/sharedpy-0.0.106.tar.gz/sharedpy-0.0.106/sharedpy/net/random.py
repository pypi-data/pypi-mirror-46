import re
from random import randrange, shuffle

from ..text.random import get_random_string

from .utils import is_valid_v4_ip




def get_random_v4_ip(first_static_octet=None, second_static_octet=None, third_static_octet=None):
    '''
    Returns a random IPv4 address.
    First, second, and third octets may optionally be specified.
    '''
    first = first_static_octet if first_static_octet else str(randrange(1, 255))
    second = second_static_octet if second_static_octet else str(randrange(0, 255))
    third = third_static_octet if third_static_octet else str(randrange(0, 255))
    forth = str(randrange(0, 255))
    return "{0}.{1}.{2}.{3}".format(first, second, third, forth)


def get_random_invalid_v4_ip():
    '''
    Returns a random v4 IP with one randomly-positioned octet value above the allowable range
    '''
    octets = [str(randrange(256, 999)), str(randrange(0, 255)), str(randrange(0, 255)), str(randrange(0, 255))]
    shuffle(octets)
    return ".".join(octets)


def find_all_valid_v4_ips(data):
    '''
    Searches the supplied string for all instances of valid IP addresses. Returns all that are found.
    Returns None if no valid v4 IPs are found
    '''
    # Find all potential IP addresses (including potentially invalid)
    pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    all = re.findall(pattern, data)
    
    # Filter down to those that are valid
    valid = [x for x in all if is_valid_v4_ip(x)]
    
    return valid or None


def get_random_mac():
    '''
    Returns a random MAC address.
    Value is random - does not conform to assigned vendor prefixes.
    '''
    return get_random_string(12, "ABCDEF0123456789")
