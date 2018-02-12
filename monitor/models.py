from django.db import models

# Create your models here.


class RadioStation(models.Model):
    """
    Model for radio stations, identified uniquely by their name
    """
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)


class Performer(models.Model):
    """
    Model for perfomers, identified uniquely by their name
    """
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)


class Song(models.Model):
    """
    Model for songs
    """
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    performer = models.ForeignKey(Performer, related_name='songs', on_delete=models.CASCADE)


class Play(models.Model):
    """
    Model for plays
    """
    song = models.ForeignKey(Song, related_name='plays', on_delete=models.CASCADE)
    radio_station = models.ForeignKey(RadioStation, related_name='plays', on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()


