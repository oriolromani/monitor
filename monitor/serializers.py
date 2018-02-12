from rest_framework import serializers
from monitor.models import RadioStation, Performer, Song, Play


class RadioStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioStation
        fields = ('id', 'created', 'name')


class PerformerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performer
        fields = ('id', 'created', 'name')


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'created', 'title')


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ('id', 'song', 'radio_station', 'start_time', 'end_time')



