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


def serialize_top_songs(songs, plays, songs_previous_week, plays_previous_week):
    """
    Serialize top songs according to the format defined in requirements
    :param songs:
    :param plays:
    :param songs_previous_week:
    :param plays_previous_week:
    :return:
    """
    result = []
    for rank, song in enumerate(songs):
        song_data = {"title": song.title,
                     "performer": song.performer.name,
                     "plays": plays.filter(song=song).count(),
                     "rank": rank}
        if song in songs_previous_week:
            previous_plays = plays_previous_week.filter(song=song).count()
            previous_rank = list(songs_previous_week).index(song)
        else:
            previous_plays = 0
            previous_rank = None
        song_data["previous_plays"] = previous_plays
        # check in which position the song was last week
        song_data["previous_rank"] = previous_rank

        result.append(song_data)
    return {"code": 0,
            "result": result}

