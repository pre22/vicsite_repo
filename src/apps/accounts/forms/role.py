from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ..models import Role

User = get_user_model()


class RoleCreationForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'


class AddBulkUserToRoleUpdateForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = User.objects.exclude(groups__in=[self.instance])

    class Meta:
        model = Role
        fields = [
            'users',
        ]