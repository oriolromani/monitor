from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from monitor.models import RadioStation, Performer, Song, Play
from monitor.serializers import RadioStationSerializer, PerformerSerializer, SongSerializer, PlaySerializer


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
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['POST'])
def add_play(request):
    """
    Insert a new play, if radio station, performer or song don't exist, create them
    :param request:
    :return:
    """
    serializer = PlaySerializer(data=request.data)
    if serializer.is_valid() and all(key in request.data for key in ('title', 'performer', 'channel')):
        performer, _ = Performer.objects.get_or_create(name=request.data["performer"])
        song, _ = Song.objects.get_or_create(title=request.data["title"], performer=performer)
        radio_station, _ = RadioStation.objects.get_or_create(name=request.data["channel"])
        _, created = Play.objects.get_or_create(song=song, radio_station=radio_station,
                                                start=request.data["start"], end=request.data["end"])
        if created:
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.data, status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
