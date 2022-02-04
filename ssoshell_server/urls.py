"""ssoshell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

admin.autodiscover()
admin.site.login_template = 'admin/login_custom.html'

urlpatterns = [
    re_path('^', include('ssoshell_server.user.urls')),
    re_path('^admin/', admin.site.urls),
    re_path(r'^auth/', include('ssoshell_server.oidc_authentication.urls')),
    re_path(r'^device/', include('ssoshell_server.device_auth.urls')),
    re_path('^host/', include('ssoshell_server.host.urls')),
]