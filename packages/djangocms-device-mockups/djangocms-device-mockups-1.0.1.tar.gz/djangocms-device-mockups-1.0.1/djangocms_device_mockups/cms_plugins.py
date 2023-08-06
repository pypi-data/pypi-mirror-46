# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import DeviceMockup
from .forms import DeviceMockupForm

class DeviceMockupPlugin(CMSPluginBase):
    model = DeviceMockup
    name = _('Device Mockup')
    module = _('Generic')
    render_template = 'djangocms_device_mockups/device-mockup.html'
    form = DeviceMockupForm
    allow_children = True

    fieldsets = (
        (None, {
            'fields': (
                'device',
                'orientation',
                'colour'
            )
        }),
        (_('Advanced'), {
            'classes': ('collapse',),
            'fields': (
                ('id_name',
                 'additional_classes',
                 'attributes',
                 ),
            ),
        }),
    )


plugin_pool.register_plugin(DeviceMockupPlugin)
