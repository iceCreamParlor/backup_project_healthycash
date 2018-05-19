# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, View, CreateView
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import datetime
from django.contrib.auth import get_user_model
from .models import Profile, Group, GroupInvite
from healthclub.models import HealthClub, HealthDiary
from .forms import RegisterNormalForm, RegisterMasterForm

User = get_user_model()

def group(request):
    user = request.user
    groups = user.is_group.all()
    group_all = Group.objects.all()
    groupinvites = GroupInvite.objects.filter(Q(new_member = user) & Q(confirmed = False)).all()
    
    notgroups = []
    for group in group_all:
        if user not in group.members.all() and group.public:
            notgroups.append(group)
    context = {'groups' : groups, 'notgroups' : notgroups, 'groupinvites' : groupinvites}
    return render(request, 'group.html', context)

def group_invite_accept(request, pk):
    group_invite = GroupInvite.objects.get(id = pk)
    group_invite.confirmed = True
    group_invite.save()
    group_invite.delete()
    group = group_invite.group
    group.members.add(request.user)
    group.save()
    
    return HttpResponseRedirect(reverse('profiles:group'))

def group_invite_decline(request, pk):
    group_invite = GroupInvite.objects.get(id = pk)
    group_invite.confirmed = True
    group_invite.save()
    group_invite.delete()
    
    return HttpResponseRedirect(reverse('profiles:group'))
    
def group_detail(request, pk):
    group = Group.objects.get(id = pk)
    groupname = group.name
    groupid = group.id
    group_masters = group.group_masters.all()
    members = group.members.all().order_by('-profile__exercised')
    context = {'groupname' : groupname, 'groupid' : groupid, 'members' : members, 'group_masters' : group_masters}
    return render(request, 'group_detail.html', context)

def add_group_master(request, groupid, userid):
    new_master = User.objects.get(id = userid)
    group = Group.objects.get(id = groupid)
    group.group_masters.add(new_master)
    group.save()
    return HttpResponseRedirect(reverse('profiles:group_detail', kwargs={'pk' : groupid}))

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

def group_register(request, pk):
    group = Group.objects.get(id = pk)
    if request.user not in group.members.all():
        group.members.add(request.user)
    return HttpResponseRedirect('/profiles/group/detail/{}/'.format(pk))

def group_update_confirm(request, pk):
    if request.method=='POST':
        group = Group.objects.get(id=pk)
        groupname = request.POST.get("groupname")
        username = request.POST.getlist("username")
        public = str(request.POST.get("public"))
        if public=="private":
                group.public = False

        group.name = groupname
        for user in username:
            new_user = User.objects.get(username = user)
            
            check = GroupInvite.objects.filter(
                inviter = request.user,
                new_member = new_user,
                group = group,
                confirmed = False
            )
            if len(check) == 0:
                group_invite = GroupInvite.objects.create(
                    inviter = request.user,
                    new_member = new_user,
                    group = group,
                    confirmed = False
                )
                group_invite.save()
        group.save()
        return HttpResponseRedirect('/profiles/group/detail/{}/'.format(pk))

def group_exit(request, pk):
    group = Group.objects.get(id=pk)
    user_id = request.user.id
    group.members.set(group.members.all().exclude(id=user_id))
    group.group_masters.set(group.group_masters.all().exclude(id=user_id))
    group.save()
    if len(group.members.all()) == 0:
        group.delete()
    return HttpResponseRedirect('/profiles/group/')

def group_create(request):
    users = Profile.objects.filter(is_health_master=False).all()
    same_healthclub_users = users.filter(healthclub = request.user.profile.healthclub)
    healthclub = request.user.profile.healthclub
    context = {'users' : users, 'same_healthclub_users' : same_healthclub_users, 'healthclub' : healthclub}

    return render(request, 'group_create.html', context)

def group_create_confirm(request):
    context = {}
    
    if request.method=="POST":
        name = request.POST.get("groupname")
        username = request.POST.getlist("username")
        search_ids = request.POST.getlist("search_ids")
        public = request.POST.get("public")
        group = Group.objects.create(name = name)
        
        if public == "private":
                group.public = False
                
        for search_id in search_ids:
            new_user = User.objects.get(username = search_id)
            
            groupinvite = GroupInvite.objects.create(
                inviter = request.user,
                new_member = new_user,
                confirmed = False,
                group = group
            )
            groupinvite.save()
            #group.members.add(new_user)
            
        for user in username:
            new_user = User.objects.get(username = user)
            
            groupinvite = GroupInvite.objects.create(
                inviter = request.user,
                new_member = new_user,
                confirmed = False,
                group = group
            )
            groupinvite.save()
            #group.members.add(new_user)
        group.members.add(request.user)
        group.group_masters.add(request.user)
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
    context = {'profile' : profile, 'username' : user.username, 'record' : record, 'real_name' : user.profile.real_name}
    return render(request, 'mypage.html', context)

# Create your views here.
class RegisterViewNormal(CreateView):
    form_class = RegisterNormalForm
    template_name = 'registration/register_normal.html'
    success_url = '/login/'
    
class RegisterViewMaster(CreateView):
    form_class = RegisterMasterForm
    template_name = 'registration/register_master.html'
    success_url = '/login/'
