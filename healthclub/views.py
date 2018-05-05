# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.views.generic import DetailView, View, CreateView, UpdateView, ListView

from .models import(
    HealthClub,
    HealthDiary,
)
from profiles.models import Profile

from .forms import HealthclubCreateForm

@login_required(login_url = "/login")
def healthclub_payment_confirm(request, pk=None):
    healthclub = HealthClub.objects.all().get(id=pk)
    request.user.profile.healthclub = healthclub
    request.user.profile.save()
    return HttpResponseRedirect("/")
    
@login_required(login_url = "/login")
def healthclub_payment(request, pk):
    healthclub = HealthClub.objects.all().get(id=pk)
    context = { 
        'healthclub_id' : healthclub.id,
        'user_name' : request.user.profile.real_name,
        'email' : request.user.profile.email , 
        'master_name' : healthclub.name, 
        'master' : healthclub.master, 
        'price' : healthclub.price, 
        'address' : healthclub.address,
    }
    # healthclub = HealthClub.objects.get('healthclub_id')
    # request.user.profile.healthclub = healthclub
    # request.user.save()
    return render(request, 'healthclub/payment.html', context)

class HealthClubDetailView(DetailView):
    model = HealthClub

class HealthClubListView(ListView):
    
    def get_queryset(self):
        return HealthClub.objects.all().order_by('updated')

@login_required(login_url = "/login")
def healthclub_create(request):
    if (request.method=="POST"):
        form = HealthclubCreateForm(request.POST)
        if form.is_valid():
            user  = request.user
            price = form.cleaned_data.get("price")
            detail = form.cleaned_data.get("detail")
            healthclub = HealthClub.objects.get(master = request.user)
            healthclub.price = price
            healthclub.detail = detail
            healthclub.save()
            
            return HttpResponseRedirect("/")
    return HttpResponseRedirect("/health/create")

@login_required(login_url = "/login")
def qrcode_check_save(request):
    healthclub_id = request.GET.get('healthclub_id')
    user = request.user
    healthclub = HealthClub.objects.get(id = healthclub_id)
    timestamp = datetime.now()

    print('hello')
    obj = HealthDiary.objects.create(
        user = user,
        healthclub = healthclub,
        timestamp = timestamp,
    )
    obj.save()
    record = HealthDiary.objects.filter(user=user)
    context = {'record' : record}
    return render(request, 'healthclub/healthclub_record.html', context)


@login_required(login_url = "/login")
def qrcode_check(request):
    context = {}
    return render(request, 'healthclub/qrcode_check.html', context)
    
def healthclub_register(request):
    context={}
    return render(request, 'healthclub/healthclub_register.html', context)