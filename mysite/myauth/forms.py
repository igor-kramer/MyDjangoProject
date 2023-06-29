from django import forms

from myauth.models import Profile


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]



