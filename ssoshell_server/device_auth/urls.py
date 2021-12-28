# users/urls.py

from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^init', views.init, name="init"),
    path(r"open/<slug:token>", views.open, name="open"),
    path("method/<slug:methodname>", views.method, name="method"),
    re_path(r"^return", views.retn, name="return"),
    path(r"callback/<slug:token>", views.callback, name="callback")
]