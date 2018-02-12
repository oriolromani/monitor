from django.conf.urls import url
from monitor import  views

urlpatterns = [
    url(r'^add_channel/$', views.add_channel, name='add_channel'),
    url(r'^add_performer/$', views.add_performer, name='add_performer'),
]
