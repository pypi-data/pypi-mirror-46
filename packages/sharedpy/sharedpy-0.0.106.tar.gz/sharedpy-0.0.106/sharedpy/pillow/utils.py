from io import BytesIO
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS

from .validation import is_valid_gpslatituderef, is_valid_gpslongituderef, is_valid_latitudelongitude_structure

# https://pillow.readthedocs.org/en/latest/reference/Image.html
# Exif tags descriptions: http://www.exiv2.org/tags.html




def extract_gps_lat_lng_exif_tags(gps_exif_data):
    '''
    Extracts the latitude and longitude tags of interest from the specified GPS EXIF data
    Returns: gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref
    '''
    return gps_exif_data.get("GPSLatitude"), gps_exif_data.get('GPSLatitudeRef'), gps_exif_data.get('GPSLongitude'), gps_exif_data.get('GPSLongitudeRef')


def gps_lat_lng_exif_values_are_valid(gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref):
    '''
    Returns True if all four GPS EXIF values are populated and formatted correctly, otherwise False
    '''
    if not gps_latitude or not is_valid_latitudelongitude_structure(gps_latitude):
        return False

    if not gps_latitude_ref or not is_valid_gpslatituderef(gps_latitude_ref):
        return False

    if not gps_longitude or not is_valid_latitudelongitude_structure(gps_longitude):
        return False

    if not gps_longitude_ref or not is_valid_gpslongituderef(gps_longitude_ref):
        return False

    return True


def get_latitude_longitude(gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref):
    '''
    Returns the latitude and longitude from the GPS Lat Lng EXIF fields
    http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/GPS.html
    '''
    lat = None
    lon = None

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_gpslatitude_gpslongitude_to_degrees(gps_latitude)
        if gps_latitude_ref != "N":                     
            lat *= -1

        lon = _convert_gpslatitude_gpslongitude_to_degrees(gps_longitude)
        if gps_longitude_ref != "E":
            lon *= -1

    return lat, lon


def get_exif_tags(pil_image):
    '''
    Returns a dictionary of exif tags within the Pillow image instance
    https://gist.github.com/erans/983821
    '''
    exif_data = {}
    try:
        for (k,v) in pil_image._getexif().items():
            tag = TAGS.get(k)
            if tag:
                if tag == "GPSInfo":
                    gps_data = {}
                    for gps_tag in v:
                        sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                        gps_data[sub_decoded] = v[gps_tag]

                    exif_data[tag] = gps_data
                else:
                    exif_data[tag] = str(v) if str(v) else None
    except AttributeError:
        pass
    return exif_data


def has_exif(pil_image):
    '''
    Returns true if any exif data is found within the Pillow image instance
    '''
    # Attempt #1 - official approach
    if hasattr(pil_image, 'info') and pil_image.info.get('exif'):
        return True
    # Attempt #2 - unofficial approach
    if hasattr(pil_image, '_getexif'):
        return pil_image._getexif() is not None
    return False      


def remove_exif(pil_image, format=None, mode=None, size=None,):
    '''
    Returns a copy of the supplied Pillow image instance (as BytesIO) with all exif data removed
    '''
    format = format if format else pil_image.format
    mode = mode if mode else pil_image.mode
    size = size if size else pil_image.size
    output = BytesIO()
    data = list(pil_image.getdata())
    clean_pil_image = Image.new(mode, size)
    clean_pil_image.putdata(data)
    clean_pil_image.save(output, format)
    clean_pil_image.close()
    output.seek(0)
    return output


def create_thumbnail(pil_image, maximum_thumb_dimension):
    '''
    Returns a thumbnail (a new Pillow instance) of the supplied Pillow image instance
    Note: Copies any EXIF data
    '''
    maximum_image_dimension = max(pil_image.height, pil_image.width)
    if maximum_thumb_dimension > maximum_image_dimension:
        raise ValueError("Maximum dimension of thumbnail ({0}) cannot exceed maximum dimension of original image ({1})".format(maximum_thumb_dimension, maximum_image_dimension))
    thumbnail = pil_image.copy()
    thumbnail.thumbnail((maximum_thumb_dimension, maximum_thumb_dimension), Image.ANTIALIAS)
    return thumbnail


def get_orientation_code(pil_image):
    '''
    Returns rotation code which indicates how the image is rotated
    Returns None if photo does not have exif tag information, or does not have orientation data

    Create test jpeg file with orientation exif tag set: exiftool.exe -Orientation="Rotate 90 CW" test.jpg
    Acceptable orientation codes for exiftool.exe: http://owl.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html
    '''
    if not has_exif(pil_image):
        return None

    for code, name in ExifTags.TAGS.items():
        if name == 'Orientation':
            return pil_image._getexif().get(code, None)

    return None


def flip_horizontal(pil_image): # Orientation code 2
    return pil_image.transpose(Image.FLIP_LEFT_RIGHT)


def rotate_180(pil_image): # Orientation code 3
    return pil_image.transpose(Image.ROTATE_180)


def flip_vertical(pil_image): # Orientation code 4
    return pil_image.transpose(Image.FLIP_TOP_BOTTOM)


def transpose(pil_image): # Orientation code 5
    return rotate_90(flip_horizontal(pil_image))


def rotate_270(pil_image): # Orientation code 6
    return pil_image.transpose(Image.ROTATE_270)


def transverse(pil_image): # Orientation code 7
    return rotate_90(flip_vertical(pil_image))


def rotate_90(pil_image): # Orientation code 8
    return pil_image.transpose(Image.ROTATE_90)


def apply_orientation(pil_image, orientation_code):
    '''
    Appropriately rotates an image based on the orientation code (obtain by calling get_orientation_code())
    Returns the image, and True or False if the image was transposed
    https://stackoverflow.com/questions/4228530/pil-thumbnail-is-rotating-my-image
    '''
    if orientation_code == 1:
        pass
    elif orientation_code == 2:
        pil_image = flip_horizontal(pil_image)
    elif orientation_code == 3:
        pil_image = rotate_180(pil_image)
    elif orientation_code == 4:
        pil_image = flip_vertical(pil_image)
    elif orientation_code == 5:
        pil_image = transpose(pil_image)
    elif orientation_code == 6:
        pil_image = rotate_270(pil_image)
    elif orientation_code == 7:
        pil_image = transverse(pil_image)
    elif orientation_code == 8:
        pil_image = rotate_90(pil_image)
    else:
        raise ValueError("Unrecognised orientation code '{}'".format(orientation_code))
    
    return pil_image, 2 <= orientation_code <= 8 # https://stackoverflow.com/a/13628825


def _convert_gpslatitude_gpslongitude_to_degrees(value):
    '''
    Helper function to convert the GPS coordinates stored in the EXIF GPSLatitude or GPSLongitude to degrees in float format
    Don't call directly, use get_latitude_longitude()
    '''
    deg_num, deg_denom = value[0]
    d = float(deg_num) / float(deg_denom)

    min_num, min_denom = value[1]
    m = float(min_num) / float(min_denom) if min_denom != 0 else 0

    sec_num, sec_denom = value[2]
    s = float(sec_num) / float(sec_denom) if sec_denom != 0 else 0
    
    return d + (m / 60.0) + (s / 3600.0)
