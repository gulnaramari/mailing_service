from django import forms
from .models import Mailing
from django.forms import BooleanField


class StyleFormMixin:
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ScheduledMailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["first_mailing", "frequency", "clients", "message"]
        widgets = {
            "first_mailing": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class ImmediateMailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["clients", "message"]
