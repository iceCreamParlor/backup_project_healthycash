# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.views.generic import DetailView, View, CreateView, UpdateView, ListView
from django.urls import reverse
import pyqrcode
import png


from .models import(
    HealthClub,
    HealthDiary,
)
from profiles.models import Profile

from .forms import HealthclubCreateForm


@login_required(login_url = "/login")
def healthclub_payment_confirm(request, pk=None, healthclub_price=None, month=None):
    healthclub = HealthClub.objects.all().get(id=pk)
    healthclub.member += 1
    healthclub.save()
    print(HealthClub.objects.all().get(id=pk).member)
    user = request.user.profile
    user.healthclub = healthclub
    user.healthclub_price = healthclub_price
    user.start_date = datetime.now()
    user.expire_date = datetime.now()+relativedelta(months=int(month))
    user.unit_cash = int(int(healthclub_price) / (int(month)*30) * 0.09)
    user.save()
    print(user.expire_date)
    return HttpResponseRedirect(reverse('profiles:mypage'))
    
    
# 이미 가입된 헬스장 있으면 가입 거부
@login_required(login_url = "/login")
def healthclub_payment(request):
    context = {}
    if request.method == 'POST':
        health_id = request.POST.get("health_id")
        price = request.POST.get("price")
        if price == None:  # Did not Select Radio Button
            return HttpResponseRedirect("/healthclub/detail/{}".format(health_id))
        price = int(price)
        month = price%100
        price = int((price - month)/100)
        
        healthclub = HealthClub.objects.all().get(id=health_id)
        context = { 
            'healthclub_id' : healthclub.id,
            'user_name' : request.user.profile.real_name,
            'email' : request.user.profile.email , 
            'master_name' : healthclub.name, 
            'master' : healthclub.master, 
            'healthclub_price' : price, 
            'address' : healthclub.address,
            'month' : month,
        }
        expire_date = request.user.profile.expire_date
        if expire_date==None or expire_date<datetime.now():
            return render(request, 'healthclub/payment.html', context)
        context["message"] = "사용 가능한 이용권이 남아있습니다. 그래도 결제를 진행하시겠습니까?"
    return render(request, 'healthclub/payment.html', context)

class HealthClubDetailView(DetailView):
    model = HealthClub
     
class HealthClubListView(ListView):
    
    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            return HealthClub.objects.filter(Q(name__icontains=search) | Q(address__icontains=search) | Q(detail__icontains=search)).order_by('updated')
        return HealthClub.objects.all().order_by('updated')

@login_required(login_url = "/login")
def healthclub_create(request):
    if (request.method=="POST"):
        form = HealthclubCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user  = request.user
            price1 = form.cleaned_data.get("price1")
            price2 = form.cleaned_data.get("price2")
            price3 = form.cleaned_data.get("price3")
            price6 = form.cleaned_data.get("price6")
            price12 = form.cleaned_data.get("price12")
            photo  = form.cleaned_data.get("photo")
            detail = form.cleaned_data.get("detail")
            
            healthclub = HealthClub.objects.get(master = request.user)
            healthclub.price1 = price1
            healthclub.price2 = price2
            healthclub.price3 = price3
            healthclub.price6 = price6
            healthclub.price12 = price12
            healthclub.photo = photo
            healthclub.detail = detail
            
            url = 'https://healthycash-heejae-kim.c9users.io/healthclub/qrcode_check_save?healthclub_id='+str(healthclub.id)
            qrcode = pyqrcode.create(url)
            qrcode_name = 'media/qrcode/healthclub_qrcode_'+str(healthclub.id) + '.png'
            qrcode.png(qrcode_name, scale=4)
            healthclub.qrcode = qrcode_name
            healthclub.save()
            
            return HttpResponseRedirect("/")
    return HttpResponseRedirect("/healthclub/create")

@login_required(login_url = "/login")
def qrcode_check_save(request):
    healthclub_id = request.GET.get('healthclub_id')
    user = request.user
    healthclub = HealthClub.objects.get(id = healthclub_id)
    timestamp = datetime.now()
    
    healthclub_check = user.profile.healthclub
    last_record = HealthDiary.objects.filter(user=request.user)
    
    if len(last_record) == 0:  # First Record
        if healthclub == healthclub_check:
            obj = HealthDiary.objects.create(
                user = user,
                healthclub = healthclub,
                timestamp = timestamp,
            )
            obj.save()
            user.profile.cash += user.profile.unit_cash
            user.profile.save()
            
            return HttpResponseRedirect(reverse('profiles:mypage'))
        else:
            context = {'message' : '이 헬스장은 회원님의 계정과 연동되지 않았습니다.'}
            return render(request, 'healthclub/qrcode_check.html', context)
    else:   
        last_record = last_record.order_by('-timestamp')[0].timestamp
        last_record = str(last_record.year)+'/'+str(last_record.month)+'/'+str(last_record.day)
        today = datetime.now()
        today = str(today.year)+'/'+str(today.month)+'/'+str(today.day)
    
        
        if last_record==today:
            context = {'message' : '오늘 이미 출석체크를 하셨습니다. 욕심 ㄴㄴ'}
            return render(request, 'healthclub/qrcode_check.html', context)
        elif healthclub == healthclub_check:
            obj = HealthDiary.objects.create(
                user = user,
                healthclub = healthclub,
                timestamp = timestamp,
            )
            obj.save()
            user.profile.cash += user.profile.unit_cash
            user.profile.save()
            
            return HttpResponseRedirect(reverse('profiles:mypage'))
        else:
            context = {'message' : '이 헬스장은 회원님의 계정과 연동되지 않았습니다.'}
            return render(request, 'healthclub/qrcode_check.html', context)

@login_required(login_url = "/login")
def qrcode_check(request):
    context = {}
    return render(request, 'healthclub/qrcode_check.html', context)
    
def mypage(request):
    healthclub = HealthClub.objects.get(master = request.user)
    healthdiary = HealthDiary.objects.filter(healthclub = healthclub)
    
    
    context = {
            'healthclub'  : healthclub,
            'healthdiary' : healthdiary,
            'qrcode_url'  : '/media/qrcode/healthclub_qrcode_'+str(healthclub.id)+'.png',
    }
    return render(request, 'healthclub/healthclub_mypage.html', context)