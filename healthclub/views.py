# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.views.generic import DetailView, View, CreateView, UpdateView, ListView
from django.urls import reverse

from .models import(
    HealthClub,
    HealthDiary,
)
from profiles.models import Profile

from .forms import HealthclubCreateForm

@login_required(login_url = "/login")
def healthclub_payment_confirm(request, pk=None, healthclub_price=None):
    healthclub = HealthClub.objects.all().get(id=pk)
    request.user.profile.healthclub = healthclub
    request.user.profile.healthclub_price = healthclub_price
    request.user.profile.save()
    return HttpResponseRedirect(reverse('profiles:mypage'))
    
    
# 이미 가입된 헬스장 있으면 가입 거부
@login_required(login_url = "/login")
def healthclub_payment(request):
    context = {}
    if request.method == 'POST':
        health_id = request.POST.get("health_id")
        price = request.POST.get("price")
        if price == None:
            return HttpResponseRedirect("/healthclub/detail/{}".format(health_id))
        healthclub = HealthClub.objects.all().get(id=health_id)
        context = { 
            'healthclub_id' : healthclub.id,
            'user_name' : request.user.profile.real_name,
            'email' : request.user.profile.email , 
            'master_name' : healthclub.name, 
            'master' : healthclub.master, 
            'healthclub_price' : price, 
            'address' : healthclub.address,
        }

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
            price1 = form.cleaned_data.get("price1")
            price2 = form.cleaned_data.get("price2")
            price3 = form.cleaned_data.get("price3")
            price6 = form.cleaned_data.get("price6")
            price12 = form.cleaned_data.get("price12")

            detail = form.cleaned_data.get("detail")
            healthclub = HealthClub.objects.get(master = request.user)
            healthclub.price1 = price1
            healthclub.price2 = price2
            healthclub.price3 = price3
            healthclub.price6 = price6
            healthclub.price12 = price12

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