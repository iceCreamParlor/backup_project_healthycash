# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.
class HealthClub(models.Model):
    name = models.CharField(max_length=120)
    
    def __str__(self):
        return self.name

class HealthDiary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    healthclub = models.ForeignKey(HealthClub)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "user : "+self.user.username+" | " + "healthclub :" + self.healthclub.name + " | " + "date : " +str(self.timestamp)

class User_Healthclub(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    healthclub = models.ForeignKey(HealthClub)
    registerdate = models.DateTimeField(auto_now=True)