from django.conf.urls import url
from monitor import  views

urlpatterns = [
    url(r'^add_channel$', views.add_channel, name='add_channel'),
    url(r'^add_performer$', views.add_performer, name='add_performer'),
    url(r'^add_song$', views.add_song, name='add_song'),
    url(r'^add_play$', views.add_play, name='add_play'),
    url(r'^get_song_plays$', views.get_song_plays, name='get_song_plays'),
    # url(r'^get_channel_plays$', views.get_channel_plays, name='get_channel_plays'),
]
