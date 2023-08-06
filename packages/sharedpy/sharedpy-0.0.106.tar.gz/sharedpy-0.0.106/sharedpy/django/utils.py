import csv
import random
import hashlib
from io import BytesIO
from datetime import timedelta

from django.urls import reverse
from django.core.cache import cache
from django.http.response import StreamingHttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.cache import cache
from django.db import connection, connections
from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.utils.timezone import make_aware, get_current_timezone, localtime
from django.contrib import messages
from django.contrib.messages import get_messages
from PIL import Image as PilImage
from ipware.ip import get_real_ip, get_ip

from sharedpy.pillow.utils import remove_exif

from ..net.utils import is_valid_v4_ip




def get_client_useragent(request):
    '''
    Returns the user agent, if present, from request meta 
    '''
    return request.META.get('HTTP_USER_AGENT', None)


def get_model_random_pk(model_class):
    '''
    Returns a randomly selected pk of the model
    Highly inefficient
    '''
    ids = list(model_class.objects.values_list('pk', flat=True))
    return random.choice(ids)


def get_days_ago(days):
    '''
    Returns the current datetime minus the specified number of days ago
    '''
    return localtime(timezone.now()) - timedelta(days=days)


def is_in_future(value):
    '''
    Django environment only!
    Returns true if the datetime value is in the future (local timezone aware)
    '''
    return value > localtime(timezone.now())


def is_in_past(value):
    '''
    Django environment only!
    Returns true if the datetime value is in the past (local timezone aware)
    '''
    return value < localtime(timezone.now())


def make_naive_datetime_tz_aware(value):
    '''
    Django environment only!
    Makes a naive datetime aware of its timezone
    '''
    return make_aware(value, get_current_timezone())


def is_admin_page(request):
    '''
    Returns True if the request path is an admin page
    '''
    return request.path.startswith(reverse('admin:index'))


def get_admin_list_url(app_name, table_name):
    '''
    Returns the URL of the Django admin change list page for the specified model (table name)
    '''
    admin_url_name = 'admin:{0}_{1}_changelist'.format(app_name.lower(), table_name.lower())
    return reverse(admin_url_name)


def get_admin_change_url(app_name, table_name, id):
    '''
    Returns the URL of the Django admin change form for the specified record
    '''
    admin_url_name = 'admin:{0}_{1}_change'.format(app_name.lower(), table_name.lower())
    return reverse(admin_url_name, args=(id,))


def clear_cache():
    '''
    Attempts to clear all django cache from all supported cache systems
    https://djangosnippets.org/snippets/2854/
    '''
    try:
        cache._cache.flush_all()
    except AttributeError:
        pass

    try:
        cache._cache.clear()
    except AttributeError:
        pass

    try:
        cache._expire_info.clear()
    except AttributeError:
        pass


def close_all_db_connections():
    '''
    Closes current DB connections so new connections will be established when next requested
    https://stackoverflow.com/questions/8242837/django-multiprocessing-and-database-connections
    '''
    connections.close_all()


def close_db_connection():
    '''
    Closes the current DB connection
    https://stackoverflow.com/questions/8242837/django-multiprocessing-and-database-connections
    '''
    connection.close()


def construct_csv_response_stream(data_to_stream, row_headers, row_display_delegate, filename):
    '''
    Streams a CSV data response.
    data_iterable: may be list of iterables or preferably queryset
    row_header: list of column titles
    row_display: delegate to output and process each row's data. Must have single argument to receive row data iterable
    filename: name of file visible to the client
    http://aeguana.com/blog/csv-export-data-for-django-model/
    https://docs.djangoproject.com/en/dev/howto/outputting-csv/#s-streaming-large-csv-files
    '''
    def stream(headers, data):
        if headers:
            yield headers
        for obj in data:
            yield row_display_delegate(obj)

    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in stream(row_headers, data_to_stream)), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="{0}.csv"'.format(filename)
 
    return response


class Echo(object):
    '''
    An object that implements just the write method of the file-like interface. Used with construct_csv_response_stream
    '''
    def write(self, value):
        '''
        Write the value by returning it, instead of storing in a buffer
        '''
        return value


def get_form_choices_display(choices, value):
    '''
    Same functionality as django's get_foo_display() but this will work with form 'choices' not just models
    '''
    return dict(choices)[int(value)]


def get_static_url(filename):
    return static(filename)


def cache_get_or_set(key, method_to_get_value):
    '''
    Django inbuilt cache.get_or_set is horribly slow
    key: key for value within cache system
    method_to_get_value: method to invoke that will return live value in the absence of value in the cache. Method must not take any arguments, and must return only a single value
    https://docs.djangoproject.com/en/1.10/topics/cache/#basic-usage
    https://docs.djangoproject.com/en/dev/topics/db/queries/#caching-and-querysets
    https://docs.djangoproject.com/en/dev/topics/cache/#the-low-level-cache-api
    https://docs.djangoproject.com/en/1.10/topics/cache/#the-per-site-cache
    '''
    cached = cache.get(key)
    if not cached:
        val = method_to_get_value()
        cache.set(key, val)
        return val
    return cached


def get_model_class_from_contenttype_id(contenttype_id):
    '''
    Returns the model class of the given content type ID
    '''
    return ContentType.objects.get_for_id(contenttype_id).model_class()


def get_contenttype_id_from_model_class(model_class):
    '''
    Returns the content type ID of the given model class
    '''
    return ContentType.objects.get_for_model(model_class).id


def verify_all_model_columns_have_data(model_class, excluded_field_names):
    '''
    Dynamically determines all column names and performs a search across each to ensure the number of null values does not equal the total number of entries - ensures at least one entry is non-null
    '''
    total_count = model_class.objects.all().count()

    if total_count == 0:
        raise Exception('No model data present')

    field_names = [x.name for x in model_class._meta.get_fields()]

    base_query = model_class.objects.all()

    for field in field_names:
        if field in excluded_field_names:
            continue
        # http://www.nomadjourney.com/2009/04/dynamic-django-queries-with-kwargs/
        # https://stackoverflow.com/a/310785
        kwargs = {'{0}__isnull'.format(field): True}
        null_count = base_query.filter(**kwargs).count()
        if null_count == total_count:
            raise Exception("Field '{0}' has no data".format(field))


def get_client_ip(request):
    '''
    Attempts to return the client's IP address if possible, otherwise None
    '''
    ip = get_real_ip(request) or get_ip(request)
    return ip if is_valid_v4_ip(ip) else None


def populate_template_with_context(template_file, context):
    '''
    Returns the string result of the template file after population with the context
    Expects context to be a dictionary.
    '''
    compiled_template = get_template(template_file)
    return compiled_template.render(context)


def pillow_to_simple_uploaded_file(pillow_image, file_name, image_format, image_content_type):
    '''
    Converts a Pillow instance to a Simple Uploaded File
    '''
    bytes_io = BytesIO()
    pillow_image.save(bytes_io, image_format)
    return bytes_io_to_simple_uploaded_file(bytes_io, file_name, image_content_type)


def bytes_io_to_simple_uploaded_file(bytes_io, file_name, content_type):
    '''
    Converts BytesIO to a Simple Uploaded File
    '''
    bytes_io.seek(0)
    return SimpleUploadedFile(file_name, bytes_io.read(), content_type=content_type)


def create_image_field_file_thumb(image_field_file, max_dimension): 
    '''
    Returns a Pillow thumbnail from an Image Field File
    Note: Returns an open instance of the file - it must must manually be closed via the .close() method
    '''
    pillow_thumb = PilImage.open(image_field_file)
    pillow_thumb.thumbnail((max_dimension, max_dimension), PilImage.ANTIALIAS)
    return pillow_thumb


def get_image_field_file_sha1(image_field_file):
    '''
    Generates and returns the SHA1 hash of an Image Field File
    '''
    image_field_file.seek(0)
    sha1 = hashlib.sha1(image_field_file.read()).hexdigest()
    image_field_file.seek(0)
    return sha1


def get_simple_uploaded_file_sha1(file):
    '''
    Generates and returns the SHA1 of a Simple Uploaded File
    '''
    file.seek(0)
    sha1 = hashlib.sha1()
    for chunk in file.chunks():
        sha1.update(chunk)
    file.seek(0)
    return sha1.hexdigest()


def delete_stale_entries(model, pks_to_keep):
    '''
    Deletes all model instances with primary keys (pks) not specified in pks_to_keep
    Returns the number of items deleted
    Note: Errors or race conditions may occur if table modifications occur during execution
    '''
    # Note: Does not use model.objects.exclude(id__in=ids_to_keep) because it can burn Postgres CPU usage with large lists and cant use with SQLite because of max field limitations
    stale = 0
    if model.objects.all().count() != len(pks_to_keep):
        for item in model.objects.all():
            if item.pk not in pks_to_keep:
                item.delete()
                stale += 1
    return stale


def message_once_only(request, level, message, extra_tags=None):
    '''
    Ensures the supplied message is added only once - does not add the message if it already exists
    If extra_tags is specified only one instance of a message containing the extra_tags will be allowed
    '''
    current_messages = get_messages(request)

    if extra_tags:
        if extra_tags in [m.extra_tags for m in get_messages(request)]:
            return

    if message in [m.message for m in get_messages(request)]:
        return

    messages.add_message(request, level, message, extra_tags=extra_tags)


def get_sanitised_image(image, image_name, image_content_type):
    """
    Returns image as a SimpleUploadedFile with all exif data removed
    Note that if the image has been modified but not yet saved the image processed will be the new unsaved image, not the existing image
    Must be used when saving a new file, a modified file, or to generate a sanitised image for hash comparison (to determine if is a duplicate of an image already uploaded)
    """
    with PilImage.open(image) as pil_img:
        clean_image_bytesio = remove_exif(pil_img, pil_img.format.lower(), pil_img.mode, pil_img.size)
        clean_image_simple_uploaded_file = bytes_io_to_simple_uploaded_file(clean_image_bytesio, image_name, image_content_type)
        pil_img.close()
        clean_image_bytesio.close()
    return clean_image_simple_uploaded_file
