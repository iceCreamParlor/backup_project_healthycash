from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from .views import(
    qrcode_check,
    qrcode_check_save,
    healthclub_create,
    HealthClubListView,
    HealthClubDetailView,
    healthclub_payment,
    healthclub_payment_confirm,
    mypage,
    healthclub_detail_review_create,
    HealthClubCreateView,
)

urlpatterns = [
    url(r'^mypage/$', mypage),
    url(r'^qrcode_check/$', qrcode_check),
    url(r'^qrcode_check_save/$', qrcode_check_save),
    url(r'^create/$', HealthClubCreateView.as_view(), name='create'),
    url(r'^create/confirm/$', healthclub_create, name ='create_confirm'),
    url(r'^list/$', HealthClubListView.as_view(), name='list'),
    url(r'^detail/(?P<pk>\d+)/$', HealthClubDetailView.as_view(), name='detail'),
    url(r'^payment/(?P<pk>\d+)/$', healthclub_payment, name = 'payment'),
    url(r'^payment/confirm/(?P<pk>\d+)/(?P<healthclub_price>\d+)/(?P<month>\d+)/', healthclub_payment_confirm, name = 'payment_confirm'),
    url(r'^healthclubdetail_reply/(?P<pk>\d+)/$', healthclub_detail_review_create, name = 'healthclub_detail_review_create'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
