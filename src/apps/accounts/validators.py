import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


def validate_username(username):
    pattern = re.compile(r'^\w+$', re.I)
    if pattern.match(username) is None:
        raise ValidationError(
            _('Username contains invalid character(s)'),
            code='invalid_username_character'
        )


def validate_username_or_email(username_or_email):
    if '@' in username_or_email:
        validate_email(username_or_email)
    else:
        validate_username(username_or_email)