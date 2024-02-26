from django import forms
from django.db import models


class CustomImageWidget(forms.widgets.ClearableFileInput):
    template_name = "inputs/image_input.html"

    def __init__(self, **kwargs):
        super(CustomImageWidget, self).__init__(**kwargs)

class CustomImage(forms.fields.ImageField):
    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.setdefault('id', 'customInputField')
        return attrs

    def __init__(self, *args, **kwargs):
        super(CustomImage, self).__init__(*args, **kwargs)

class CustomImageField(models.ImageField):

    def formfield(self, **kwargs):
        kwargs['form_class'] = CustomImage
        kwargs["widget"] = CustomImageWidget
        return super(CustomImageField, self).formfield(**kwargs)
    



