import re
import json
import string
import hashlib
import csv
from io import StringIO

import exrex




def contains(value, allowed_chars):
    '''
    Returns True if every char in value is present in alllowed_chars, otherwise False
    Both arguments should be of type string
    '''
    for c in value:
        if not c in allowed_chars:
            return False
    return True


def get_string_sha1(value, encoding='utf-8'):
    '''
    Returns the SHA1 hash of the specified string
    '''
    h = hashlib.sha1()
    h.update(value.encode(encoding))
    return h.hexdigest()


def get_string_md5(value, encoding='utf-8'):
    '''
    Returns the MD5 hash of the specified string
    '''
    h = hashlib.md5()
    h.update(value.encode(encoding))
    return h.hexdigest()


def get_string_bytes_size(value, encoding='utf-8'):
    '''
    Returns the size of the specified string in bytes
    http://stackoverflow.com/questions/4013230/how-many-bytes-does-a-string-have
    '''
    return len(value.encode(encoding))


def remove_extended_characters(value):
    '''
    Removes all characters aside from decimal 32 through 126 (retains all standard US keyboard characters)
    In other words this replaces all non-printable characters and the whole extended ASCII range (127 - 255)
    http://www.danshort.com/ASCIImap/
    '''
    return ''.join([i if ord(i) < 127 and ord(i) > 31 else '' for i in value])


def get_extended_characters():
    '''
    Returns a string of ASCII characters from 160 to 255, typically non-standard characters
    This method is intended to mostly be used during character cleansing, testing, and random string generation
    '''
    return "".join([chr(x) for x in range(160, 256)])


def re_split(value, regex):
    '''
    Performs the same functionality as str.split() however this differs by:
    - this accepts a regular expression pattern, and
    - all empty items are excluded
    Returns a list
    '''
    items = re.split(regex, value)
    return list(filter(None, items))


def strip_unprintable(value):
    '''
    Removes all non-printable characters from the supplied string
    Printable characters include digits, ascii_letters, punctuation, and whitespace.
    https://docs.python.org/3/library/string.html#string.printable
    '''
    return ''.join([x for x in value if x in string.printable])


def get_pretty_print_string(value, max_length):
    '''
    Returns a 'pretty print' string:
    If the string character length is less than the max_length argument the whole string is returned
    If the string character length exceeds the max_length argument the string is truncated to (max_length - 3) and '...' is appended
    max_length must be greater than 3
    '''
    if max_length <= 3:
        raise ValueError('max_length argument must be greater than 3')

    return (value[:max_length - 3] + '...') if len(value) > max_length else value


def data_to_csv_string(data):
    '''
    Converts a single row of data to CSV string.
    Generally expects argument to be a list of strings.
    https://stackoverflow.com/questions/9157314/python-write-data-into-csv-format-as-string-not-file
    '''
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(data)
    return si.getvalue().strip('\r\n')


def sanitise_hex_string(value):
    '''
    Returns only hexidecimal characters present within value
    '''
    return ''.join([x for x in value if x in string.hexdigits])


def get_empty_str_if_none(value):
    '''
    Returns an empty string if the value is None, otherwise returns the value
    '''
    return value if value != None else ''


def safe_string_strip(value):
    '''
    Returns the supplied string with leading and trailing whitespace removed
    If the supplied argument is not of type string the argument will gracefully be returned (no exception raised)
    '''
    return value.strip() if value != None and type(value) is str else value


def safe_string_upper(value):
    '''
    Returns the supplied string converted to upper case
    If the supplied argument is not of type string the argument will gracefully be returned (no exception raised)
    '''
    return value.upper() if value != None and type(value) is str else value


def parse_csv_file(csv_file_path, encoding, ignore_first_row=True, ignore_empty_rows=True, delimiter=','): # TODO: Tests
    '''
    Reads a multiline CSV file's content and returns it as a list of lists
    '''
    with open(csv_file_path, 'r', encoding=encoding) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=delimiter)
        data = list(csv_reader)
        if ignore_first_row:
            del data[0]
        return [x for x in data if x] if ignore_empty_rows else data


def parse_csv_object(data, encoding, ignore_first_row=True, ignore_empty_rows=True, delimiter=',', split='\n'): # TODO: Tests
    '''
    Decodes a multiline CSV object and returns it as a list of lists
    '''
    csv_reader = csv.reader([x.strip() for x in data.decode(encoding).split(split)], delimiter=delimiter)
    data = list(csv_reader)
    if ignore_first_row:
        del data[0]
    return [x for x in data if x] if ignore_empty_rows else data


def generate_regex_text(re_pattern, min_chars, max_chars, strip=True, max_attempts=1000):
    '''
    Generates random text that matches the supplied regular expression pattern
    '''
    i = 0
    text = None
    while True:
        text = exrex.getone(re_pattern, limit=max_chars)
        if strip:
            text = text.strip()
        if len(text) >= min_chars and len(text) <= max_chars:
            return text
        if i > max_attempts:
            raise EOFError('Too many attempts generating regex text')
        i += 1


def string_contains_continuous_characters(value):
    '''
    Returns True if the the value passed consists entirely of continuous characters, either forward or reverse.
    This is based on the ASCII decimal value of each character.
    For example, all the following qill return True: '1234567', 'defghij', '98765'
    http://www.asciitable.com/
    '''
    previous_forward = None
    previous_backward = None

    for c in value:

        # Create history
        if not previous_forward  and not previous_backward:
            previous_forward = previous_backward = ord(c)
            continue

        # Compare current to history
        if ord(c) != previous_forward + 1 and ord(c) != previous_backward - 1:
            return False
        previous_forward = previous_backward = ord(c)
    return True


def is_valid_json(str):
    '''
    Returns True if the argument string can be parsed as JSON, otherwise False
    '''
    try:
        json.loads(str)
        return True
    except (ValueError, TypeError):
        return False
