# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, View, CreateView
from django.shortcuts import render, redirect

from .models import Profile
from healthclub.models import HealthClub
from .forms import RegisterNormalForm, RegisterMasterForm

def mypage(request):
    user = request.user
    profile = Profile.objects.all().get(user=user)
    context = {'profile' : profile, 'username' : user.username}
    return render(request, 'mypage.html', context)

# Create your views here.
class RegisterViewNormal(CreateView):
    form_class = RegisterNormalForm
    template_name = 'registration/register_normal.html'
    success_url = '/'
    
class RegisterViewMaster(CreateView):
    form_class = RegisterMasterForm
    template_name = 'registration/register_master.html'
    success_url = '/'

    # def dispatch(self, *args, **kwargs):
    #     if self.request.user.is_authenticated():
    #         return redirect("/logout")
    #     return super(RegisterView, self).dispatch(*args, **kwargs)