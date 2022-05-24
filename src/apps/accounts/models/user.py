import datetime

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.cache import cache
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..managers.user import UserManager
from ..validators import validate_username

SEX = (
    ("Male", "Male"),
    ("Female", "Female"),
)

OCCUPATION = (
    ("Student", "Student"),
    ("Employed", "Employed"),
    ("Unemployed", "Unemployed"),
    ("Self-Employed", "Self-Employed"),
    ("Others", "Others"),
)

STATUS = (
    ("Pending", "Pending"),
    ("Failed", "Failed"),
    ("Completed", "Completed"),
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('e-mail'),
        unique=True
    )
    username = models.CharField(
        verbose_name=_('username'),
        max_length=25,
        unique=True,
        db_index=True,
        validators=[validate_username]
    )
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    occupation = models.CharField(max_length=100, choices=OCCUPATION)
    sex = models.CharField(max_length=20, choices=SEX)
    is_admin = models.BooleanField(
        verbose_name=_('Is admin'),
        default=False
    )
    is_superuser = models.BooleanField(
        verbose_name=_('Is superuser'),
        default=False
    )
    is_active = models.BooleanField(
        verbose_name=_('Is active'),
        default=True
    )
    phone = models.CharField(
        verbose_name=_('Telephone'),
        max_length=20,
        blank=True
    )
    country = models.CharField(
        verbose_name=_('Country'),
        max_length=50,
        blank=True
    )
    about = models.TextField(
        verbose_name=_('About you'),
        help_text=_('Brief description of yourself'),
        blank=True
    )
    date_created = models.DateTimeField(
        verbose_name=_('Registration date'),
        auto_now_add=True,
        help_text=_('Date and time of registration')
    )
    last_modified = models.DateTimeField(
        verbose_name=_('Last modified'),
        auto_now=True,
        help_text=_('Date and time of profile last modification')
    )
    last_seen = models.DateTimeField(
        verbose_name=_('Last time seen'),
        default=timezone.now,
        help_text=_('Date and time user was last active'),
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP Address'),
        blank=True,
        null=True,
        help_text=_('IP Address of last login')
    )
    visits = models.PositiveIntegerField(default=0)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_constraint_user_email_username'
            )
        ]
        indexes = [
            models.Index(
                fields=['id', 'username'],
                name='idx_user_id_username'
            )
        ]
        ordering = ['email', 'username']

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def get_short_name(self):
        return self.username

    @property
    def get_full_name(self):
        return self.email

    def last_seen_cache(self):
        return cache.get(f'seen_{self.username}')

    def is_online(self):
        if self.last_seen_cache():
            now = timezone.now()
            return now <= self.last_seen_cache() + datetime.timedelta(seconds=settings.USER_LASTSEEN_TIMEOUT)
        else:
            return False

    def online(self):
        return 'online' if (check_online := self.is_online()) else 'offline'

    def __str__(self):
        return f'{self.username} - {self.email}'