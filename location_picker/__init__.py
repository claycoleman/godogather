from django import forms
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


# Set this if not using staticfiles
STATIC_URL = getattr(settings, 'LOCATION_PICKER_STATIC_URL', '%slocation_picker/' % settings.STATIC_URL)

class LocationPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
            '%slocation_picker.css' % STATIC_URL,
            )
        }
        js = (
            '%sjquery-1.11.3.min.js' % (settings.STATIC_URL + 'js/'),
            '%slocation_picker.js' % STATIC_URL,
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(LocationPickerWidget, self).__init__(attrs=attrs)


    def render(self, name, value, attrs=None):
        if None == attrs:
            attrs = {}
        attrs['class'] = 'location_picker'
        return super(LocationPickerWidget, self).render(name, value, attrs)

class LocationField(models.CharField):

    def __init__(self, *args, **kwargs):
        if not 'max_length' in kwargs:
            kwargs['max_length'] = 255
        super(LocationField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = LocationPickerWidget
        return super(LocationField, self).formfield(**kwargs)
        
    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect the _actual_ field.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        # That's our definition!
        return (field_class, args, kwargs)

    def validate(self, value, obj):
        super(LocationField, self).validate(value, obj)
        try:
            x, y = value.split(',')
            float(x.strip()), float(y.strip())
        except:
            raise ValidationError('Bad coordinate format - should be ll,la. Example: 43.5343,172.6236')
