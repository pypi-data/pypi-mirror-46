# -*- coding: utf-8 -*-
"""
Enables the user to add style plugin that displays a html tag with
the provided settings from the style plugin.
"""
from __future__ import unicode_literals

from cms.models import CMSPlugin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from djangocms_attributes_field.fields import AttributesField
from django.utils.text import slugify


@python_2_unicode_compatible
class DeviceMockup(CMSPlugin):

    device = models.CharField(
        verbose_name=_('Device'),
        max_length=100,
    )

    orientation = models.CharField(
        verbose_name=_('Orientation'),
        blank=True,
        null=True,
        max_length=100,
    )

    colour = models.CharField(
        verbose_name=_('Colour'),
        blank=True,
        null=True,
        max_length=100,
    )

    # Default id/classes/attributes
    # --------------------------------
    id_name = models.CharField(
        verbose_name=_('ID name'),
        blank=True,
        null=True,
        max_length=255,
    )
    additional_classes = models.CharField(
        verbose_name=_('Additional classes'),
        blank=True,
        max_length=255,
        help_text=_('Additional comma separated list of classes '
            'to be added to the element e.g. "row, column-12, clearfix".'),
    )
    attributes = AttributesField(
        verbose_name=_('Attributes'),
        blank=True,
        excluded_keys=['class', 'id', 'style'],
    )

    def clean(self):
        if self.id_name:
            valid_id_name = slugify(self.id_name)
            self.id_name = valid_id_name

    def get_additional_classes(self):
        return ' '.join(item.strip() for item in self.additional_classes.split(',') if item.strip())

    @property
    def get_id_name(self):
        return self.id_name or str(self.pk)

    def __str__(self):
        return self.get_id_name
