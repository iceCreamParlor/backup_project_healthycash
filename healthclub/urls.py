from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from .views import(
    qrcode_check,
    qrcode_check_save,
    healthclub_register,
)

urlpatterns = [
    url(r'^qrcode_check/', qrcode_check),
    url(r'^qrcode_check_save/', qrcode_check_save),
    url(r'^register/', healthclub_register),

]