# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("get_certificate", views.get_certificate, name="get_certificate"),
    path("get_principals/<slug:servername>", views.get_principals, name="get_principals"),
]