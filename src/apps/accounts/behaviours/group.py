from django.contrib.auth.models import Group as BaseGroupModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class GroupMixin(BaseGroupModel):
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        help_text=_('Brief description of what the role is all about')
    )
    slug = models.SlugField(
        verbose_name=_('URL identifier'),
        unique=True,
        editable=False,
        blank=True
    )

    class Meta:
        abstract = True