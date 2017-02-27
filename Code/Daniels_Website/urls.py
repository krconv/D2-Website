"""
Django URL Configuration for Daniels Website
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('pages.urls')),
    url(r'^admin/', admin.site.urls),
]
