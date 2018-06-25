from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q 
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from healthclub.models import HealthClub

@login_required(login_url = "/login")
def home(request):
    return HttpResponseRedirect("/healthclub/list")
    # healthclubs = HealthClub.objects.all()
    # keywords = set()
    # hkeywords = set()
    # for healthclub in healthclubs:
    #     if len(healthclub.address) >= 12:
    #         address_short = healthclub.address[0:12] + ".."
    #     temp = healthclub.name + "(" + address_short + ")"
    #     hkeywords.add(temp)
    #     addresses = healthclub.address.split(' ')
    #     for address in addresses:
    #         keywords.add(address)

    # context = {'keywords' : keywords, 'healthclubs' : hkeywords}
    
    # return render(request, 'home.html', context)