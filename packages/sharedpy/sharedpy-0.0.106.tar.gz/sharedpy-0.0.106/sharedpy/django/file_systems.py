import os
import uuid

from django.core.exceptions import SuspiciousFileOperation
from django.core.files.storage import FileSystemStorage

from sharedpy.io.utils import get_layered_path

from common.models import Configuration




class RandomUuidFileSystemStorage(FileSystemStorage):
    """
    Assigns a random available UUID-derived filename and assigns a layered path
    """

    def get_available_name(self, name, max_length=None):
        """
        Returns a filename based on the name parameter that's free and available for new content to be written to on the target storage system.
        If a free unique filename cannot be found after 10 iterations a SuspiciousFileOperation exception will be raised.
        max_length argument is ignored - it's required as per method definition
        Only the file extension is used from the supplied name argument
        https://docs.djangoproject.com/en/1.11/ref/files/storage/#django.core.files.storage.FileSystemStorage
        https://docs.djangoproject.com/en/1.11/ref/files/storage/#the-filesystemstorage-class
        """
        for _ in range(10):
            _, extension = os.path.splitext(name.lower())
            new_filename = str(uuid.uuid4()).replace('-', '') + extension
            new_filename_with_path = get_layered_path(new_filename, Configuration.get_solo().image_directory_storage_depth)
            if not self.exists(new_filename_with_path):
                return new_filename_with_path
        return SuspiciousFileOperation("Failed to find available new UUID-based filename")


    def get_valid_name(self, name):
        """
        Returns an available random filename
        When used with a model ImageField the order of calls are: generate_filename() --> get_valid_name(). get_available_name() is not called (by default) during a save operation.
        """
        return self.get_available_name(name)
