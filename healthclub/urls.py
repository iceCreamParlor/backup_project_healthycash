from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from .views import(
    qrcode_check,
    qrcode_check_save,
    healthclub_register,
    healthclub_create,
    HealthClubListView,
    HealthClubDetailView,
    healthclub_payment,
    healthclub_payment_confirm,
)

urlpatterns = [
    url(r'^qrcode_check/$', qrcode_check),
    url(r'^qrcode_check_save/$', qrcode_check_save),
    url(r'^register/$', healthclub_register),
    url(r'^create/$', TemplateView.as_view(template_name='healthclub/healthclub_create.html')),
    url(r'^create/confirm/$', healthclub_create, name ='create_confirm'),
    url(r'^register/$', healthclub_register),
    url(r'^list/$', HealthClubListView.as_view(), name='list'),
    url(r'^detail/(?P<pk>\d+)/$', HealthClubDetailView.as_view(), name='detail'),
    url(r'^payment/$', healthclub_payment, name = 'payment'),
    url(r'^payment/confirm/(?P<pk>\d+)/(?P<healthclub_price>\d+)/', healthclub_payment_confirm, name = 'payment_confirm'),

]