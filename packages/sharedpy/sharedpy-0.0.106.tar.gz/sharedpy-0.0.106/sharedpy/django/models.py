from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.utils import NestedObjects
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.apps import apps




class DateTimeFieldTz(models.DateTimeField):
    '''
    Simply a DateTimeField with local time applied to value retrieved from database (which appears to always be stored in DB as UTC)
    http://stackoverflow.com/a/34082786
    '''
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return None
        else:
            return timezone.localtime(value)


def get_or_none(classmodel, **kwargs):
    '''
    Returns a model instance based on kwargs. If matching instance isn't found returns None
    '''
    try:
        return classmodel.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None


def get_related_models(model_instance): 
    '''
    Returns a list of all model classes this model has a relationship with
    Must be performed on a model instance rather than a model class - model instance fields will detect external model relationships.
    '''
    related_models = []
    for field in model_instance._meta.get_fields():
        if field.related_model:
            related_models.append(field.related_model)
    return related_models


def has_active_relation(model_instance): 
    '''
    Returns True if at least one other model instance has a relationship with this instance
    Intended to be used to determine if this object can safely be deleted without any consequential cascade deletions
    Customised version of https://stackoverflow.com/questions/26659023/deletion-objects-that-is-used-as-foreign-key and https://gist.github.com/vonorm/8617378
    '''
    for field in model_instance._meta.get_fields():
        if field.related_model: # not all field types have a related model
            related = field.related_model.objects.filter(**{field.field.name: model_instance})[:1].values_list('pk', flat=True) # Only get PK of first result to make SELECT query as minimal as possible. Using .exists() performs a SELECT with all attributes specified.
            if len(related) > 0:
                return True
    return False


def get_nested_objects(model_instance, db_name='default'):
    '''
    Returns all nested objects that directly relate to a model instance. These objects may be affected through cascade deletion if model_instance were to be deleted.
    '''
    collector = NestedObjects(using=db_name)
    collector.collect([model_instance,])
    return collector.nested()


def find_stale_items(pks, model_class):
    '''
    Returns a list of pks (a subset of pks passed in) for all model instances that have no relations
    Intended for use with removing stale items that are no longer referenced from List Tables (http://mark.random-article.com/musings/db-tables.html)
    Race condition may occur - this should only be run while the database is offline or while no data is being updated or created that could affect the model_class
    '''
    stale_pks = []      
    for pk in pks:   
        instance = model_class.objects.get(pk=pk)
        if not has_active_relation(instance) and len(get_nested_objects(instance)) == 1: # Use two different methods (for extra paranoia) to ensure no relations exist
            stale_pks.append(pk)
    return stale_pks


def get_model_field(app_label, model_name, field_name):
    '''
    Returns the model meta field specified
    '''
    return next(x for x in apps.get_model(app_label, model_name)._meta.fields if x.name == field_name)


def get_model_field_minvaluevalidator_value(app_label, model_name, field_name):
    '''
    Returns the limit_value from a model meta field MinValueValidator
    '''
    model_field = get_model_field(app_label, model_name, field_name)
    return next(x.limit_value for x in model_field.validators if type(x) == MinValueValidator)


def get_model_field_maxvaluevalidator_value(app_label, model_name, field_name):
    '''
    Returns the limit_value from a model meta field MaxValueValidator
    '''
    model_field = get_model_field(app_label, model_name, field_name)
    return next(x.limit_value for x in model_field.validators if type(x) == MaxValueValidator)


def get_model_field_minlengthvalidator_value(app_label, model_name, field_name):
    '''
    Returns the limit_value from a model meta field MinLengthValidator
    '''
    model_field = get_model_field(app_label, model_name, field_name)
    return next(x.limit_value for x in model_field.validators if type(x) == MinLengthValidator)


def get_model_field_maxlengthvalidator_value(app_label, model_name, field_name):
    '''
    Returns the limit_value from a model meta field MaxLengthValidator
    '''
    model_field = get_model_field(app_label, model_name, field_name)
    return next(x.limit_value for x in model_field.validators if type(x) == MaxLengthValidator)


def get_model_field_regexvalidator_value(app_label, model_name, field_name):
    '''
    Returns the regex pattern from a model meta field RegexValidator
    '''
    model_field = get_model_field(app_label, model_name, field_name)
    return next(x.regex.pattern for x in model_field.validators if type(x) == RegexValidator)
