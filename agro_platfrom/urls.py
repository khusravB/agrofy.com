from django.contrib import admin
from django.urls import path, include, re_path
from .yasg import urlpatterns as doc_urls
from rest_framework import routers
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('djoser.urls')),  # new
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # new
    path('api/v1/', include('app.urls')),
] + doc_urls
