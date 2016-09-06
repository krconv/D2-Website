from django.conf.urls import url
import django_cas_ng
from . import views


urlpatterns = [
    url(r'^$', views.home_page),
    url(r'^home$', views.home_page, name='home'),
    url(r'^links$', views.links_page, name='useful_links'),
    url(r'^meet$', views.meet_us_page, name='meet_us'),
    url(r'^contact$', views.contact_page, name='contact_us'),
    url(r'^login/$', django_cas_ng.views.login),
    url(r'^logout/$', django_cas_ng.views.logout), 
]
