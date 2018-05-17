from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q 
from django.urls import reverse

from healthclub.models import HealthClub

def home(request):
    healthclubs = HealthClub.objects.all()
    keywords = set()
    for healthclub in healthclubs:
        keywords.add(healthclub.name)
        addresses = healthclub.address.split(' ')
        for address in addresses:
            keywords.add(address)
    context = {'keywords' : keywords}
    
    return render(request, 'home.html', context)