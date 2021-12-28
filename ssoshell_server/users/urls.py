# users/urls.py

from django.urls import include, re_path
from . import views

urlpatterns = [
    re_path(r"^accounts/logout", include("django.contrib.auth.urls")),
    re_path(r"success", views.success, name="success"),
]