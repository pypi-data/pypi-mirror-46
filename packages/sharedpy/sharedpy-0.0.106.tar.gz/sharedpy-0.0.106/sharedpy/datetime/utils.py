import datetime

from django.template.defaultfilters import pluralize




def convert_date_to_datetime(date):
    '''
    Returns a datetime instance with date populated from date instance
    '''
    return datetime.datetime(date.year, date.month, date.day)


def generate_days_offset(dt, days_difference):
    '''
    Returns a datetime with days offset by days_difference
    Days difference may be positive or negative whole number 
    '''
    return dt + datetime.timedelta(days=days_difference)


def days_hours_minutes_seconds(value):
    '''
    Returns a timedelta as days, hours, minutes, seconds
    '''
    minutes, seconds = divmod(value.total_seconds(), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return int(days), int(hours), int(minutes), int(seconds)


def humanize_timedelta(td):
    '''
    Converts a timedelta to an english-friendly representation
    '''
    d, h, m, s = days_hours_minutes_seconds(td)
    result = []
    if d:
        result.append("{0} day{1}".format(d, pluralize(d)))
    if h:
        result.append("{0} hour{1}".format(h, pluralize(h)))
    if m:
        result.append("{0} minute{1}".format(m, pluralize(m)))
    if s:
        result.append("{0} second{1}".format(s, pluralize(s)))

    return ", ".join(result) if any([d, h, m, s]) else "< 1 second"


def get_latest_date(*dates):
    '''
    Returns the latest date or datetime of all args specified
    Returns None if all dates are None
    '''
    return max(x for x in dates if x is not None) if not dates.count(None) == len(dates) else None


def days_diff(date1, date2):
    '''
    Returns the number of days difference between the two dates.
    Number of days will always be positive, regardless of order of date arguments
    '''
    return abs(date2-date1).days
