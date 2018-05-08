# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from healthclub.models import HealthClub
from django.core.urlresolvers import reverse

User = get_user_model()
mail = []



class RegisterNormalForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
  
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    real_name = forms.CharField(max_length = 120)
    sex       = forms.CharField(max_length = 120)
    email      = forms.CharField(max_length = 120)
    
    class Meta:
        model = User
        fields = ('username', 'sex', 'email', 'real_name', 'password1', 'password2')

    def clean_email(self):
        global mail
        email = self.cleaned_data["email"]
        qs = User.objects.filter(email__iexact=email)

        if qs.exists():
            raise forms.ValidationError("해당 이메일은 이미 회원가입 되어있습니다")
        else:
            mail.append(email)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        global mail
        # Save the provided password in hashed format
        user = super(RegisterNormalForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        user.save()
        profile = Profile.objects.create(
            user=user, 
            real_name = self.cleaned_data["real_name"], 
            sex = self.cleaned_data["sex"],
            email = mail[len(mail)-1],
        )
        profile.save()
        mail = []
       

        return user
        
class RegisterMasterForm(forms.ModelForm):
  
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    real_name = forms.CharField(max_length = 120)
    sex       = forms.CharField(max_length = 120)
    email      = forms.CharField(max_length = 120)
    healthclub_name = forms.CharField(max_length = 120)
    healthclub_address = forms.CharField(max_length = 200)
    
    class Meta:
        model = User
        fields = ('username', 'sex', 'email', 'real_name', 'password1', 'password2', 'healthclub_name', 'healthclub_address')

    def clean_email(self):
        global mail
        email = self.cleaned_data["email"]
        qs = Profile.objects.filter(email__iexact=email)
        
        if qs.exists():
            raise forms.ValidationError("해당 이메일은 이미 회원가입 되어있습니다.")
        else:
            mail.append(email)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        global mail
        # Save the provided password in hashed format
        user = super(RegisterMasterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        user.save()
        profile = Profile.objects.create(
            user=user, 
            real_name = self.cleaned_data["real_name"], 
            sex = self.cleaned_data["sex"],
            email = mail[len(mail)-1],
            is_health_master = True,
        )
        profile.save()
        
        healthclub = HealthClub.objects.create(
            master    = user,
            name      = self.cleaned_data["healthclub_name"],
            address   = self.cleaned_data["healthclub_address"],
            member    = 0,
        )
        healthclub.save()
        mail = []
        return user