import datetime




class Timer(object):
    '''
    Basic throw-away timer. Originally based on https://pypi.python.org/pypi/simple_timer
    '''
    def __init__(self):
        '''
        Initialises the timer
        '''
        self._start_time = datetime.datetime.now()
        
        
    @property
    def duration(self):
        '''
        Returns the duration (seconds) since the object was initialised
        '''
        timedelta = datetime.datetime.now() - self._start_time
        return float('{}.{}'.format(timedelta.seconds, timedelta.microseconds))


    @property
    def timedelta(self):
        '''
        Returns the timedelta since the object was initialised
        '''
        return datetime.datetime.now() - self._start_time
