# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, View, CreateView
from django.shortcuts import render
from django.shortcuts import redirect


from .forms import RegisterNormalForm, RegisterMasterForm

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