from django.forms.models import ModelForm
from django import forms
from .consts import *
from django.utils.translation import ugettext_lazy as _


class DeviceMockupForm(ModelForm):
    device = forms.ChoiceField(choices=DEVICE_CHOICES)

    orientation = forms.ChoiceField(choices=ORIENTATION_CHOICES)

    colour = forms.ChoiceField(choices=COLOUR_CHOICES)

    def clean(self):
        cleaned_data = super(DeviceMockupForm, self).clean()
        device = cleaned_data.get("device")
        orientation = cleaned_data.get("orientation")
        colour = cleaned_data.get("colour")

        if device in DEVICE_DICT:
            allowed_values = DEVICE_DICT[device]

            if orientation not in allowed_values['orientation']:
                raise forms.ValidationError(
                    _('Invalid orientation: %(orientation)s, Allowed Values are: %(allowed)s'),
                    code='invalid',
                    params={'orientation': orientation,
                            'allowed': allowed_values['orientation']}, )

            if colour not in allowed_values['colour']:
                raise forms.ValidationError(
                    _('Invalid colour: %(colour)s, Allowed Values are: %(allowed)s'),
                    code='invalid',
                    params={'colour': colour,
                            'allowed': allowed_values['colour']}, )

        else:
            raise forms.ValidationError(
                _('Invalid device: %(device)s'),
                code='invalid',
                params={'device': device}, )
