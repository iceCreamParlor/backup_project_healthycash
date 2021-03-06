# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model
from profiles.models import Profile
from healthclub.models import HealthClub, HealthClubDetailReply


User = get_user_model()
class HealthclubCreateForm(forms.Form):
    price1    = forms.IntegerField(label='Price')
    price2    = forms.IntegerField(label='Price')
    price3    = forms.IntegerField(label='Price', required=False)
    price6    = forms.IntegerField(label='Price', required=False)
    price12   = forms.IntegerField(label='Price', required=False)
    photo     = forms.ImageField(required=False)
    detail    = forms.CharField(label='Detail', widget = forms.Textarea)
    address   =  forms.CharField(label='address')
    
class HealthClubDetailReplyForm(forms.ModelForm):
    
    class Meta:
        model = HealthClubDetailReply
        fields = ['reply']

