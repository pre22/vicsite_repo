from django import forms
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.utils.translation import gettext_lazy as _

from .user import BaseUserCreationForm
from ..validators import validate_username_or_email


class AuthenticationForm(BaseAuthenticationForm):
    auto_id = False

    username = forms.CharField(
        label=_('E-mail or username'),
        validators=[validate_username_or_email],
        widget=forms.TextInput(attrs={'autocomplete': True})
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        for field in self.fields:
            placeholder = _(self.fields[field].label.title())
            self.fields[field].widget.attrs.update({
                'id': f'floating{field.title()}',
                'placeholder': f'{placeholder}',
                'class': 'form-control rounded-4',
            })


class UserRegistrationForm(BaseUserCreationForm):
    about_you = forms.CharField(
        label=_('About you'),
        required=False,
        max_length=200,
        widget=forms.Textarea
    )