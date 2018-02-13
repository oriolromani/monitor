import json
from dateutil.parser import parse as date_parse
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from monitor.models import RadioStation, Performer, Song, Play
from monitor.serializers import RadioStationSerializer, PerformerSerializer, SongSerializer, PlaySongSerializer,\
    PlayChannelSerializer


@api_view(['POST'])
def add_channel(request):
    """
    Insert a new radio station
    :param request:
    :return:
    """
    serializer = RadioStationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def add_performer(request):
    """
    Insert a new performer
    :param request:
    :return:
    """
    serializer = PerformerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_song(request):
    """
    Insert a new song, if performer does not exist, create it
    :param request:
    :return:
    """
    serializer = SongSerializer(data=request.data)
    if serializer.is_valid() and 'performer' in request.data:
        performer, _ = Performer.objects.get_or_create(name=request.data['performer'])

        _, created = Song.objects.get_or_create(performer=performer, title=request.data['title'])
        if created:
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.data, status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def validate_add_play_data(request):
    parameters = ('title', 'performer', 'channel', 'start', 'end')
    return all(key in request.data for key in parameters)


@api_view(['POST'])
def add_play(request):
    """
    Insert a new play, if radio station, performer or song don't exist, create them
    :param request:
    :return:
    """
    if validate_add_play_data(request):
        performer, _ = Performer.objects.get_or_create(name=request.data["performer"])
        song, _ = Song.objects.get_or_create(title=request.data["title"], performer=performer)
        radio_station, _ = RadioStation.objects.get_or_create(name=request.data["channel"])
        _, created = Play.objects.get_or_create(song=song, radio_station=radio_station,
                                                start=request.data["start"], end=request.data["end"])
        if created:
            return Response(status.HTTP_201_CREATED)
        return Response(status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_song_plays(request):
    """
    Get the plays for a song between two dates
    :param request:
    :return:
    """
    data = request.GET
    try:
        song = Song.objects.get(title=data['title'], performer__name=data['performer'])
        start_date = date_parse(data['start'])
        end_date = date_parse(data['end'])
        plays = song.plays.filter(start__range=(start_date, end_date))
        serializer = PlaySongSerializer(plays, many=True)
        data = {"result": serializer.data,
                "code": 0}
        return Response(data)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_channel_plays(request):
    """
    Get all the songs played on a given channel between two dates
    :param request:
    :return:
    """
    data = request.GET
    try:
        start_date = date_parse(data['start'])
        end_date = date_parse(data['end'])
        plays = Play.objects.filter(radio_station__name=data['channel'],
                                    start__range=(start_date, end_date)).select_related('song')
        serializer = PlayChannelSerializer(plays, many=True)
        data = {"result": serializer.data,
                "code": 0}
        return Response(data)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_top(request):
    """
    Get a top 40 for a given week and a list of channels: a list of 40 songs ordered by the number of
    times they were broadcast. For each song, provide their performer, playcount and the position
    they had the previous week.
    :param request:
    :return:
    """
    data = request.GET
    start = date_parse(data["start"])
    end = start + timedelta(days=6)
    songs = Song.objects.annotate(num_plays=Count('plays')).filter(
        plays__in=Play.objects.filter(radio_station__name__in=json.loads(data["channels"]),
                                      start__range=(start, end))).order_by('num_plays')
