from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from .views import (
    mypage, group, group_create, group_create_confirm, 
    group_detail, group_update, group_exit, group_update_confirm,
    group_register,
)


urlpatterns = [
    url(r'^mypage/', mypage, name='mypage'),
    url(r'^group/$', group, name='group'),
    url(r'^group/create/$', group_create, name='group_create'),
    url(r'^group/create/confirm/$', group_create_confirm, name='group_create_confirm'),
    url(r'^group/detail/(?P<pk>[\d]+)/$', group_detail, name='group_detail'),
    url(r'^group/update/(?P<pk>[\d]+)/$', group_update, name='group_update'),
    url(r'^group/update/confirm/(?P<pk>[\d]+)/$', group_update_confirm, name='group_update_confirm'),
    url(r'^group/register/(?P<pk>[\d]+)/$', group_register, name='group_register'),
    url(r'^group/exit/(?P<pk>[\d]+)/$', group_exit, name='group_exit'),

]
