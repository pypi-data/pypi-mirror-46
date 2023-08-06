import os
import re
import hashlib
import mimetypes
import sys
import shutil
import tempfile
import cchardet

from ..misc.utils import is_windows




def yes_to_prompt():
    '''
    Waits for 'yes' or 'no' input
    Returns True if yes is entered, otherwise False
    '''
    yes = set(['yes','y', 'ye'])
    no = set(['no','n'])
    while True:
        choice = input().lower()
        if choice in yes:
           return True
        elif choice in no:
           return False
        else:
           sys.stdout.write("Please respond with 'yes' or 'no'")


def get_mimetype(filename):
    '''
    Guesses the file mimetype based on its name
    '''
    mimetype, encoding = mimetypes.guess_type(filename)
    return mimetype


def mimetype_is_in_list(filename, mimetypes):
    '''
    Returns True if the mimetype of the file is present within the list of mimetypes
    '''
    mimetype = get_mimetype(filename)
    if mimetype:
        minetypesl = [mt.lower() for mt in mimetypes]
        return mimetype.lower() in minetypesl
    return False


def extension_is_in_list(filename, extensions):
    '''
    Returns true if the filename ends with any extension in extensions
    Each extension must contain a leading period
    Case insensitive
    '''
    basename, ext = os.path.splitext(filename.lower())
    extensions = [ext.lower() for ext in extensions]
    return ext.lower() in extensions


def get_empty_directories(root_directory):
    '''
    Recursively searches for all empty directories (contain no files or directories)
    Returns a list of all empty directories found
    '''
    results = []
    for dirpath, dirs, files in os.walk(root_directory):
        if not dirs and not files:
            results.append(dirpath)
    return results


def find_files(root_directory, regex_pattern='.*', find_matching=True):
    '''
    Recursively searches for files matching (or not matching) the regex pattern, default is all files
    Returns a list of all files found that meet the specified search criteria
    '''
    compiled_regex = re.compile(regex_pattern)
    results = []
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            file_path = os.path.join(root, file)
            if find_matching:
                if compiled_regex.search(file):
                    results.append(file_path)
            else:
                if not compiled_regex.search(file):
                    results.append(file_path)
    return results


def touch_file(filepath):
    '''
    Creates a new file
    '''
    open(filepath, 'a').close()


def get_file_sha1(filepath):
    '''
    Returns a file's SHA1 value
    '''
    BUF_SIZE = 65536  # reads in 64kb chunks
    sha1 = hashlib.sha1()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def get_layered_path(filename, depth, filename_suffix=None):
    '''
    Returns the supplied filename prefixed with a directory path based on the first number of characters of it's name (as defined in depth argument)
    Filename must only be the filename - no path
    Note that this does not create the path, nor does it validate the path
    '''
    if os.path.dirname(filename):
        raise ValueError("Filename cannot contain path")
    basename, ext = os.path.splitext(filename)
    if len(basename) == 0:
        raise ValueError("No filename specified")
    if 1 > depth:
        raise ValueError("A depth must be specified")
    if depth > len(basename):
        raise ValueError("Folder depth ({0}) cannot be greater than filename length ({1}).".format(depth, len(basename)))
    if filename_suffix:
        filename = '{0}{1}{2}'.format(basename, filename_suffix, ext) # Note that ext, if populated, will have a 'dot' prefix
    path = ''
    for x in basename[:depth]:
        path = os.path.join(path, x)
    return os.path.join(path, filename)


def ensure_dir(path):
    '''
    Attempts to create the specified path including all subdirectories
    https://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary
    '''
    d = os.path.dirname(path)
    if not os.path.exists(d):
        os.makedirs(d)


def delete_files_in_dir(dir):
    '''
    Deletes all files and directories within the specified directory
    Does not delete the directory specified
    https://stackoverflow.com/questions/185936/delete-folder-contents-in-python
    '''
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def write_temp_file(content):
    tmp = tempfile.NamedTemporaryFile(dir=tempfile.gettempdir(), delete=False)
    if not is_windows():
        os.chmod(tmp.name, 0o700) # r+w+x owner only http://www.onlineconversion.com/html_chmod_calculator.htm
    tmp.write(content)
    tmp.close()
    return tmp.name


def get_file_encoding(file_path): # TODO: Tests
    '''
    Returns the file's auto-detected encoding (best effort)
    '''
    with open(file_path, "rb") as file:
        data = file.read()
        enc = cchardet.detect(data)
        return enc['encoding']


def read_file(file_path): # TODO: Tests
    with open(file_path, 'rb') as f:
        return f.read()


def write_file(path, content, mode='wb'): # TODO: Tests
    with open(path, "wb") as f:
        f.write(content)


def append_trailing_sep(path): # TODO: Tests
    '''
    Appends a trailing slash to a string (intended for use with a directory path)
    If a trailing slash is already present an additional one will *not* be appended
    '''
    if path[-1:] != os.sep:
        return path + os.sep
    return path
