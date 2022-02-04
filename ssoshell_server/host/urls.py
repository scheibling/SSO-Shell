# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("bootstrap/", views.bootstrap_host, name="bootstrap_host"),
    path("<slug:servername>/principals", views.get_principals, name="get_principals"),
    path("ca_public_key", views.get_certificate, name="get_certificate"),
]