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


class PlaySongSerializer(serializers.ModelSerializer):
    channel = serializers.SerializerMethodField()

    class Meta:
        model = Play
        fields = ('start', 'end', 'channel')

    def get_channel(self, obj):
        return obj.radio_station.name


class PlayChannelSerializer(serializers.ModelSerializer):
    performer = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Play
        fields = ('performer', 'title', 'start', 'end')

    def get_performer(self, obj):
        return obj.song.performer.name

    def get_title(self, obj):
        return obj.song.title
