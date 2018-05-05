from django import forms
from django.contrib.auth import get_user_model
from profiles.models import Profile
from healthclub.models import HealthClub


User = get_user_model()
class HealthclubCreateForm(forms.Form):
    price1    = forms.IntegerField(label='Price')
    price2    = forms.IntegerField(label='Price')
    price3    = forms.IntegerField(label='Price')
    price6    = forms.IntegerField(label='Price')
    price12    = forms.IntegerField(label='Price')
    detail   = forms.CharField(label='Detail', widget = forms.Textarea)

