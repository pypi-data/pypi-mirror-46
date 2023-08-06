from urllib.parse import urljoin

from django.urls import reverse




class ReadOnlyAdminMixin(object):

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.get_fields() if not f.auto_created]
    
    def has_add_permission(self, *args):
        return False

    def has_delete_permission(self, *args):
        return False
    
    def get_actions(self, request):
        actions = super(ReadOnlyAdminMixin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    def save_model(self, request, obj, form, change):
        pass

    def delete_model(self, request, obj):
        pass

    def save_related(self, request, form, formsets, change):
        pass




class DeleteOnlyAdminMixin(object):

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.get_fields() if not f.auto_created]
    
    def has_add_permission(self, *args):
        return False

    def has_delete_permission(self, *args):
        return True
    
    def save_model(self, request, obj, form, change):
        pass

    def save_related(self, request, form, formsets, change):
        pass




class GetAdminUrl():
    '''
    Helper class to assist with generating admin URLs
    https://docs.djangoproject.com/en/dev/ref/contrib/admin/#admin-reverse-urls
    '''

    @staticmethod
    def index():
        return reverse('admin:index')


    @staticmethod
    def login():
        return reverse('admin:login')


    @staticmethod
    def login_with_next(next_url):
        return urljoin(GetAdminUrl.login(), '?next=', next_url)


    @staticmethod
    def logout():
        return reverse('admin:logout')


    @staticmethod
    def password_change():
        return reverse('admin:password_change')


    @staticmethod
    def password_change_done():
        return reverse('admin:password_change_done')


    @staticmethod
    def jsi18n():
        return reverse('admin:jsi18n')


    @staticmethod
    def app_list(app_label):
        return reverse('admin:app_list', args=(app_label.lower(),))


    @staticmethod
    def view_on_site(content_type_id, object_id):
        return reverse('admin: 	view_on_site', args=(content_type_id, object_id))


    @staticmethod
    def changelist(app_label, model_name):
        return reverse('admin:{}_{}_changelist'.format(app_label.lower(), model_name.lower()))


    @staticmethod
    def add(app_label, model_name):
        return reverse('admin:{}_{}_add'.format(app_label.lower(), model_name.lower()))


    @staticmethod
    def history(app_label, model_name, object_id):
        return reverse('admin:{}_{}_history'.format(app_label.lower(), model_name.lower()), args=(object_id,))


    @staticmethod
    def delete(app_label, model_name, object_id):
        return reverse('admin:{}_{}_delete'.format(app_label.lower(), model_name.lower()), args=(object_id,))


    @staticmethod
    def change(app_label, model_name, object_id):
        return reverse('admin:{}_{}_change'.format(app_label.lower(), model_name.lower()), args=(object_id,))


    @staticmethod
    def password_change(user_id):
        return reverse('admin:auth_user_password_change', args=(user_id,))
