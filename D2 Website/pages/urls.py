from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home_page),
    url(r'^home$', views.home_page, name='home'),
    url(r'^links$', views.links_page, name='useful_links'),
    url(r'^contact$', views.contact_page, name='contact_us'),
]
