from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from ucamlookup.forms import UserCreationForm
from ucamlookup.models import LookupGroup


class LookupUserAdmin(UserAdmin):
    list_display = ('username', 'last_name', 'is_staff', 'is_superuser')
    add_form = UserCreationForm
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',),
        }),
    )
    add_form_template = 'admin/auth/lookup_user/add_form.html'


if admin.site.is_registered(User):
    admin.site.unregister(User)
admin.site.register(User, LookupUserAdmin)


class LookupGroupAdmin(admin.ModelAdmin):
    list_display = ('lookup_id', 'name',)
    search_fields = ('lookup_id', 'name',)
    ordering = ('lookup_id', 'name',)
    add_form_template = 'admin/auth/lookup_group/add_form.html'

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.resolver_match.view_name == u'admin:ucamlookup_lookupgroup_add':
            self.exclude.append('lookup_id')
            self.exclude.append('name')
        else:
            self.exclude.append('name')
        return super(LookupGroupAdmin, self).get_form(request, obj, **kwargs)


if admin.site.is_registered(LookupGroup):
    admin.site.unregister(LookupGroup)
admin.site.register(LookupGroup, LookupGroupAdmin)
