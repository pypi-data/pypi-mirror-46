import csv
import operator
import itertools
from io import StringIO
from collections import OrderedDict




def remove_falsey_items(iterable):
    '''
    Removes all 'falsey' items from the supplied iterable.
    Warning: Removes zeros - this may not always be desirable behaviour
    '''
    return [x for x in iterable if x]


def unique_duplicate(iterable):
    '''
    Creates two lists derived from the supplied iterable: duplicate values and unique values
    Returns: unique, duplicate
    '''
    unique = []
    duplicate = []
    for x in iterable:
        if x in unique:
            if x not in duplicate:
                duplicate.append(x)
        else:
            unique.append(x)
    return unique, duplicate


def is_iterable(value):
    '''
    Returns true if the argument is iterable, that is, if it implements the __iter__ method
    http://anandology.com/python-practice-book/iterators.html
    '''
    try:
        iter(value)
        return True
    except TypeError:
        return False


def build_list(length, default_item_value=None):
    '''
    Returns a list with the specified number of elements all of value default_item_value
    https://stackoverflow.com/a/10712044
    '''
    return [default_item_value] * length


def divide_iterable(iterable, desired_segments=1):
    '''
    Divides iterable argument into the number of desired segments (where possible) or less depending on length of iterable
    Behaviour is different with strings: ("string", 3) == ['st','ri','ng']
    https://stackoverflow.com/a/752562/1095373
    '''
    if desired_segments > len(iterable):
        desired_segments = len(iterable)

    length = len(iterable)
    return [iterable[i*length // desired_segments: (i+1)*length // desired_segments] for i in range(desired_segments)]


def flatten_list(list_of_lists):
    '''
    Flattens (merges) a list of lists into a single list
    Note: Only flattens the top (single) level - nested lists will remain
    '''
    return list(itertools.chain(*list_of_lists))


def sort_list_of_dicts(list_of_dicts):
    '''
    Sorts a list of dictionaries by the key names of the first row
    All dictionaries MUST contain the same keys
    '''
    return [OrderedDict(sorted(x.items(), key=operator.itemgetter(0))) for x in list_of_dicts]


def list_of_dicts_to_ordered_csv(list_of_dicts, delimiter=',', lineterminator='\n'):
    '''
    Produces CSV string output with each row sorted alphabetically by key name (of the first row).
    All dictionaries MUST contain the same keys as title row and ordering is derived from key names of first dictionary.
    '''
    sorted_columns = sort_list_of_dicts(list_of_dicts)

    with StringIO() as si:
        dict_writer = csv.DictWriter(si, sorted_columns[0].keys(), delimiter=delimiter, lineterminator=lineterminator,)
        dict_writer.writeheader()
        dict_writer.writerows(sorted_columns)
        return si.getvalue().strip('\r\n')


def rename_dictionary_keys(data, mapping, default_value=None):
    '''
    Renames the dictionary's keys based on the mapping. If any 'old value' isn't present it'll be added and assigned the value of 'default_value'.
    e.g. of mapping definition: {'crap name 1':'great name 1', 'crap name 2': 'great name 2'}
    Does NOT maintain key order!
    Key name is case sensitive.
    '''
    reconstituted = {}
    for old_name, new_name in mapping.items():
        reconstituted[new_name] = data.get(old_name, default_value)
    return reconstituted


def delete_dict_entries(dict, *keys):
    '''
    Deletes all specified keys from the dictionary if they're present.
    Does not raise an exception if any key (to be deleted) is not present.
    '''
    for k in keys:
        try:
            del dict[k]
        except KeyError:
            pass
    return dict


def tag_last(iterable):
    '''
    Given some iterable, returns (last, item), where last is only true if you are on the final iteration.
    Slightly modified version of https://stackoverflow.com/a/22995806
    '''
    iterator = iter(iterable)
    gotone = False
    try:
        lookback = next(iterator)
        gotone = True
        while True:
            cur = next(iterator)
            yield False, lookback
            lookback = cur
    except StopIteration:
        if gotone:
            yield True, lookback


def merge_two_dicts(x, y):
    '''
    Returns two combined dictionaries
    '''
    return {**x, **y}
