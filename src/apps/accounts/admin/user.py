from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from ..forms.admin import UserAdminChangeForm, UserAdminCreationForm
from ..models import Role

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    readonly_fields = [
        'date_created',
        'last_modified',
        'last_login'
    ]
    list_display_links = ['email', 'username']

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'id', 'username', 'is_admin', 'is_superuser')
    list_filter = ('is_admin', 'is_superuser')
    list_editable = ('is_admin', 'is_superuser')
    fieldsets = [
        (_('Login'), {
            'fields': ('email', 'username', 'password')
        }),
        (_('Personal info'), {
            'fields': (('country'), 'about')
        }),
        (_('Permissions'), {
            'fields': ('is_admin', 'is_superuser')
        }),
        (_('Important dates'), {
            'fields': ('date_created', 'last_modified', 'last_seen')
        }),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
        (_('Permissions'), {
            'classes': ('wide',),
            'fields': ('is_admin', 'is_superuser'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id', 'username',)
    filter_horizontal = ()


__all__ = [
    'UserAdmin'
]

admin.site.unregister(Group)
admin.site.register(Role)