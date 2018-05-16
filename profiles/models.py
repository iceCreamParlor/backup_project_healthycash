# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from healthclub.models import HealthClub

User = settings.AUTH_USER_MODEL

# Create your models here.
class Profile(models.Model):
    user             = models.OneToOneField(User) # user.profile 
    email            = models.CharField(max_length = 120)
    real_name        = models.CharField(max_length = 120, null=True)
    sex              = models.CharField(max_length = 50, null=True)
    followers        = models.ManyToManyField(User, related_name='followers', blank=True)
    following        = models.ManyToManyField(User, related_name='following', blank=True)
    timestamp        = models.DateTimeField(auto_now_add=True)
    updated          = models.DateTimeField(auto_now=True)
    healthclub       = models.ForeignKey(HealthClub, null=True)
    is_health_master = models.BooleanField(default = False)
    exercised        = models.IntegerField(default = 0)
    unit_cash        = models.IntegerField(default = 0)
    cash             = models.IntegerField(default = 0)
    healthclub_price = models.IntegerField(default = 0)
    start_date       = models.DateTimeField(null=True)
    expire_date      = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.user.username.encode('utf-8')
        
class Group(models.Model):
    name             = models.CharField(max_length = 120)
    members          = models.ManyToManyField(User, related_name='is_group', blank = True)
    group_masters    = models.ManyToManyField(User, related_name='is_group_master', blank=True)
    public           = models.BooleanField(default = True)

    def __str__(self):
        return self.name.encode('utf-8')
        
class GroupInvite(models.Model):
    inviter          = models.ForeignKey(User, related_name = 'inviter')
    new_member       = models.ForeignKey(User, related_name = 'new_member')
    group            = models.ForeignKey(Group, related_name = 'group', null=True)
    confirmed        = models.BooleanField(default = False)
    
    def __str__(self):
        return self.inviter.username.encode('utf-8') + self.new_member.username.encode('utf-8')
        