from django import forms
from cabinet.models import Avatar


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['avatar']
