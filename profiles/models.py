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
    cash             = models.IntegerField(default = 0)
    healthclub_price = models.IntegerField(default = 0)

    def __unicode__(self):
        return self.user.username
        