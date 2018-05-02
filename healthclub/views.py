# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime

from .models import(
    HealthClub,
    HealthDiary,
)
# Create your views here.

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