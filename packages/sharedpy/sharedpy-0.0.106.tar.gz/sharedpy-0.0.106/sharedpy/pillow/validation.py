import re
from sharedpy.collection.utils import is_iterable
from sharedpy.number.utils import is_whole




def is_valid_latitudelongitude_structure(value):
    '''
    Returns True if value is a properly formatted EXIF value for GPSLatitude or GPSLongitude
    '''
    if not value or not is_iterable(value) or len(value) != 3: # TODO: New false tests
        return False

    for x in value:
        if len(x) != 2:
            return False
       
        if not is_whole(x[0]) or not is_whole(x[1]):
            return False

    return True


def is_valid_gpslatituderef(value):
    '''
    Returns True if value is a valid EXIF value for GPSInfo - GPSLatitudeRef
    Valid values are:
    N (+)
    S (-)
    '''
    return bool(re.match(r'^[NS]$', value))


def is_valid_gpslongituderef(value):
    '''
    Returns True if value is a valid EXIF value for GPSInfo - GPSLongitudeRef
    Valid values are:
    E (+)
    W (-)
    '''
    return bool(re.match(r'^[EW]$', value))
