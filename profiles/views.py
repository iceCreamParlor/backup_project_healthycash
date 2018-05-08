# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, View, CreateView
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth import get_user_model
from .models import Profile, Group
from healthclub.models import HealthClub, HealthDiary
from .forms import RegisterNormalForm, RegisterMasterForm

User = get_user_model()

def group(request):
    user = request.user
    groups = user.is_group.all()
    context = {'groups' : groups}
    return render(request, 'group.html', context)

def group_detail(request, pk):
    group = Group.objects.get(id = pk)
    groupname = group.name
    groupid = group.id
    members = group.members.all().order_by('profile__exercised')
    context = {'groupname' : groupname, 'groupid' : groupid, 'members' : members}
    return render(request, 'group_detail.html', context)

def group_update(request, pk):
    users = Profile.objects.filter(is_health_master=False)
    group = Group.objects.get(id=pk)
    groupname = group.name
    groupid = pk

    members=[]
    for user in users:
        if len(user.user.is_group.all().filter(id=pk)) == 0:
            members.append(user)
    context = {'users' : users, 'groupname' : groupname, 'groupid' : groupid, 'members' : members}
    return render(request, 'group_update.html', context)

def group_update_confirm(request, pk):
    if request.method=='POST':
        group = Group.objects.get(id=pk)
        groupname = request.POST.get("groupname")
        username = request.POST.getlist("username")
        group.name = groupname
        for user in username:
            new_user = User.objects.get(username = user)
            group.members.add(new_user)
        group.members.add(request.user)
        group.save()
        return HttpResponseRedirect('/profiles/group/detail/{}/'.format(pk))

def group_exit(request, pk):
    group = Group.objects.get(id=pk)
    user_id = request.user.id
    group.members.set(group.members.all().exclude(id=user_id))
    group.save()
    return HttpResponseRedirect('/profiles/group/')

def group_create(request):
    users = Profile.objects.filter(is_health_master=False)
    context = {'users' : users}
    return render(request, 'group_create.html', context)

def group_create_confirm(request):
    context = {}
    
    if request.method=="POST":
        name = request.POST.get("groupname")
        username = request.POST.getlist("username")
        group = Group.objects.create(name = name)
        for user in username:
            new_user = User.objects.get(username = user)
            group.members.add(new_user)
        group.members.add(request.user)
        group.save()

    return HttpResponseRedirect(reverse('profiles:group'))
 
def mypage(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    last_diary = HealthDiary.objects.filter(user = user)
    
    expire_date = profile.expire_date  #When expire_date Expires
    if expire_date != None:
        if expire_date < datetime.now():
            profile.healthclub = None
            profile.expire_date = None
            profile.start_date = None
            profile.save()
    if(len(last_diary)==0):
        pass
    else:
        last_diary = last_diary.last().timestamp
        if last_diary.month < datetime.now().month:
            profile.exercised = 0
    profile = Profile.objects.get(user=user)
    record = HealthDiary.objects.filter(user=user)
    context = {'profile' : profile, 'username' : user.username, 'record' : record}
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