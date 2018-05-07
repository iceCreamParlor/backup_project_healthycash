# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here
        
class HealthClub(models.Model):
    name      = models.CharField(max_length = 120)
    address   = models.CharField(max_length = 200)
    master    = models.ForeignKey(User)
    photo     = models.ImageField(blank=True)
    member    = models.IntegerField(default = 0)
    price1    = models.IntegerField(default = 0, blank = True)
    price2    = models.IntegerField(default = 0, blank = True)
    price3    = models.IntegerField(default = 0, blank = True)
    price6    = models.IntegerField(default = 0, blank = True)
    price12   = models.IntegerField(default = 0, blank = True)
    detail   = models.CharField(max_length = 1000, blank = True)
    timestamp = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name

class HealthDiary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    healthclub = models.ForeignKey(HealthClub)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "user : "+self.user.username+" | " + "healthclub :" + self.healthclub.name + " | " + "date : " +str(self.timestamp)

class User_Healthclub(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL)
    healthclub   = models.ForeignKey(HealthClub)
    registerdate = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "user : "+self.user.username+" | " + "healthclub :" + self.healthclub.name + " | " + "date : " +str(self.registerdate)