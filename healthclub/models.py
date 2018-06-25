# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here
        
class HealthClub(models.Model):
    initiated = models.BooleanField(default=False)
    name      = models.CharField(max_length = 120)
    address   = models.CharField(max_length = 200) 
    master    = models.ForeignKey(User, related_name='is_health_master')
    geometry  = models.CharField(max_length = 200, blank=True)
    photo     = models.ImageField(blank=True)
    qrcode    = models.ImageField(blank=True)
    member    = models.IntegerField(default = 0)
    price1    = models.IntegerField(blank = True, default= 0)
    price2    = models.IntegerField(blank = True, default= 0)
    price3    = models.IntegerField(blank = True, default= 0)
    price6    = models.IntegerField(blank = True, default= 0)
    price12   = models.IntegerField(blank = True, default= 0)
    detail   = models.CharField(max_length = 1000, blank = True)
    timestamp = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}'.format(self.name)

class HealthDiary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    healthclub = models.ForeignKey(HealthClub)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "user : "+self.user.username+" | " + "healthclub :" + self.healthclub.name + " | " + "date : " +str(self.timestamp)

class HealthClubDetailReply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    healthclub = models.ForeignKey(HealthClub)
    reply = models.CharField(max_length = 300)
    timestamp = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}'.format(self.user.username + ' | ' +self.healthclub.name)