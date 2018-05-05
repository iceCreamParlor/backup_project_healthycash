from django import forms
from django.contrib.auth import get_user_model
from profiles.models import Profile
from healthclub.models import HealthClub


User = get_user_model()
class HealthclubCreateForm(forms.Form):
    price    = forms.IntegerField(label='Price')
    detail   = forms.CharField(label='Detail', widget = forms.Textarea)

