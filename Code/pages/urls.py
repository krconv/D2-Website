from django.conf.urls import url
from django_cas_ng.views import login, logout
from pages.views import *

urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^home/$', home_page),
    url(r'^events/$', events_page, name='events'),
    url(r'^tools/$', tools_page, name='tools'),
    url(r'^tools/auth$', auth_page),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'), 
]
