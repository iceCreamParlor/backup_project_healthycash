from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from .views import mypage

urlpatterns = [
    url(r'^mypage/', mypage, name='mypage'),
    

]