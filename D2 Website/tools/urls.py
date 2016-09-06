from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'duty', views.duty_tool, name='duty'),
]
