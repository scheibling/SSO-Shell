# users/urls.py

from django.urls import include, re_path, path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r"^accounts/logout", include("django.contrib.auth.urls")),
    re_path(r"success", views.success, name="success"),
]