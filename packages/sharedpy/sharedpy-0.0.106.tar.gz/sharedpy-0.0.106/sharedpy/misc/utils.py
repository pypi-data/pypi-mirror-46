import sys
import subprocess
import os
import hashlib
import traceback
import importlib
import cchardet
import multiprocessing
from functools import partial
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures import as_completed

from ..collection.utils import divide_iterable



def is_bytes_object(obj):
    '''
    Returns True if the argument can be decoded (usually bytes string)
    Based on https://stackoverflow.com/a/34870210
    '''
    try:
        obj.decode()
        return True
    except AttributeError:
        return False


def add_method_to_object(obj, func_name, func): # TODO: Tests
    """
    Adds 'func' (a method) as an instance method to obj (class instance / object)
    'func_name' is the name of the method once added to the class instance / object
    """
    setattr(obj, func_name, partial(func, obj))


def get_exception_details(e):
    '''
    Gets a friendly exception message (for displaying to users) and a detailed exception message (for logging or debugging)
    Return format: friendly_message, detailed_message
    https://stackoverflow.com/a/35712784
    '''
    friendly_message = str(e).split(' <')[0] if ' <' in str(e) else str(e)
    detailed_message = "".join(traceback.format_exception(etype=type(e),value=e,tb=e.__traceback__))
    return friendly_message, detailed_message


def module_exists(name):
    '''
    Returns True if the specified module is importable within the current python environment
    '''
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False


def is_windows():  # TODO: Tests
    '''
    Returns True if the current environment is Windows, otherwise False
    '''
    return os.name == 'nt'


def get_multiprocessing_segment_count(iterable): # TODO: Tests
    '''
    Returns the most suitable number of parts an iterable should be divided by in order to achieve greatest benefit from CPU-intensive processing.
    Partner method to divide_iterable().
    '''
    return multiprocessing.cpu_count() if len(iterable) > multiprocessing.cpu_count() else len(iterable)


def get_object_sha1(object):
    ''' 
    Returns the SHA1 hexdigest for the object argument
    '''
    return hashlib.sha1(object).hexdigest()


def object_has_method(object, method_name):
    '''
    Returns True if the object's owning class contains a method called method_name
    Works for both static and instance methods
    '''
    return hasattr(object, method_name) and callable(getattr(object, method_name))


def run_cmd(cmd): # TODO: Tests
    '''
    Launches the supplied command and optionally arguments
    Returns: output, successful, error_code
    Output is all output returned by the command as a string
    Successful is a boolean indicating if the command returned an exit code of 0 (success) or other (failure)
    Error code is the return code if it is a a non-zero value, otherwise None
    '''
    output = None
    successful = None
    error_code = None
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        successful = True
    except subprocess.CalledProcessError as e:
        output = e.output
        error_code = e.returncode
        successful = False
    return output, successful, error_code


def multiprocess_iterable(worker_delegate, items_to_process, *args, close_db_conns=True, max_workers=None):  # TODO: Tests
    '''
    Manages the processing of each item in an iterable across multiple CPU cores. Divides the iterable evenly (as best as possible) and spreads the work across each segment at the same time.
    worker_delegate: Method that'll be called to perform the work. The first argument passed to worker_delegate will be a portion / segment of items_to_process. This argument may optionally be followed by *args if additional arguments must be passed.
    close_db: If used within Django and the worker_delegate interacts with any Django models this must be set to True.
    max_workers: Specify to override the default value (default: number of CPU cores).
    returns: a list of values returned from each instance of worker_delegate. If no return value is specified within worker_delegate this will be a list of None.
    
    Notes:
    Synchronous - waits for all processes to complete before returning.
    Pass only basic data types! DO NOT pass datetime variables or django model instances or querysets. If working with Django models pass the primary key or plain filter values.
    All arguments passed in or returned must go through the Pytho pickler, and therefore the data types must be picklable.
    In a normal python module the calling code must be prefixed somewhere with: "if __name__ == '__main__':"
    In a Django project this can only be called from within the thread of a management command. Also, the worker_delegate MUST reside in a different module to this method and the first two imports MUST be:
    import django
    django.setup()
    '''
    segments = divide_iterable(items_to_process, max_workers if max_workers else get_multiprocessing_segment_count(items_to_process))

    results = []
    futures = []
    with ProcessPoolExecutor(max_workers=len(segments)) as pool:

        if close_db_conns:
            from sharedpy.django.utils import close_all_db_connections # We only want to import this if working in a django environment
            close_all_db_connections()

        for segment in segments:
            futures.append(pool.submit(worker_delegate, segment, *args))

        for future in as_completed(futures):
            results.append(future.result())

        if close_db_conns:
            from sharedpy.django.utils import close_all_db_connections # We only want to import this if working in a django environment
            close_all_db_connections()

    return results


def raise_current_error():  # TODO: Tests
    '''
    Raises the most recent exception.
    Intended for use within an except block
    '''
    t, v, tb = sys.exc_info()
    raise v.with_traceback(tb)


def detect_encoding(data):
    '''
    Returns a best-effort encoding of the object
    '''
    enc = cchardet.detect(data)
    return enc['encoding']
