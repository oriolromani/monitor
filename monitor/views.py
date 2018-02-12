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