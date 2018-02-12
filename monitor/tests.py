from django.test import TestCase, Client
from django.urls import reverse

from monitor.models import RadioStation, Performer, Song, Play

# initialize the APIClient app
client = Client()


class ViewsAddTestCase(TestCase):
    """
    Test for the monitor api views
    """
    def test_add_channel(self):
        # post with data
        data = {"name": "new channel"}
        response = client.post(reverse('add_channel'), data)
        self.assertEqual(response.status_code, 201)
        # one radio station should exist
        self.assertEqual(RadioStation.objects.all().count(), 1)
        # existing radio station should have the data provided in the request
        self.assertTrue(RadioStation.objects.filter(name=data["name"]).exists())
        # if we post again with the same data, as name is unique we should get
        self.assertEqual(response.status_code, 201)
        self.assertEqual(RadioStation.objects.all().count(), 1)

    def test_add_artist(self):
        # post with data
        data = {"name": "new performer"}
        response = client.post(reverse('add_performer'), data)
        self.assertEqual(response.status_code, 201)
        # one radio station should exist
        self.assertEqual(Performer.objects.all().count(), 1)
        # existing radio station should have the data provided in the request
        self.assertTrue(Performer.objects.filter(name=data["name"]).exists())
        # if we post again with the same data, as name is unique we should get an 200
        response = client.post(reverse('add_performer'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], ['performer with this name already exists.'])

    def test_add_song(self):
        # post with data
        data = {"title": "new song", "performer": "new performer"}
        response = client.post(reverse('add_song'), data)
        self.assertEqual(response.status_code, 201)
        # one song should exist
        self.assertEqual(Song.objects.all().count(), 1)
        # a new performer should exist
        self.assertEqual(Performer.objects.all().count(), 1)
        # existing performer and song should have the data provided by the request
        self.assertTrue(Performer.objects.filter(name=data["performer"]).exists())
        self.assertTrue(Song.objects.filter(performer=Performer.objects.get(name=data["performer"]),
                                            title=data["title"]).exists())

        # post again with same data
        data = {"title": "new song", "performer": "new performer"}
        response = client.post(reverse('add_song'), data)
        self.assertEqual(response.status_code, 200)

    def test_add_play(self):
        # post with data
        data = {"title": "new song",
                "performer": "new performer",
                "channel": "new_channel",
                "start": "2014-10-21T18:41:00",
                "end": "2014-10-21T18:44:00"}
        response = client.post(reverse('add_play'), data)
        self.assertEqual(response.status_code, 201)
        # one song should exist
        self.assertEqual(Song.objects.all().count(), 1)
        self.assertTrue(Song.objects.filter(performer=Performer.objects.get(name=data["performer"]),
                                            title=data["title"]).exists())
        # one radio station should exist
        self.assertEqual(RadioStation.objects.all().count(), 1)
        # existing radio station should have the data provided in the request
        self.assertTrue(RadioStation.objects.filter(name=data["channel"]).exists())
        # one play should exist
        self.assertEqual(Play.objects.all().count(), 1)
        # existing play should have the data provided in the request
        self.assertTrue(Play.objects.get(
            song=Song.objects.get(performer=Performer.objects.get(name=data["performer"]),
                                  title=data["title"]),
            radio_station=RadioStation.objects.get(name=data["channel"]),
            start=data["start"],
            end=data["end"]))


class ViewsGetTestCase(TestCase):
    def setUp(self):
        self.performer = Performer.objects.create(name='Performer')
        self.song = Song.objects.create(performer=self.performer, title='Song')
        self.radio_station = RadioStation.objects.create(name='Radio')
        self.play1 = Play.objects.create(song=self.song, radio_station=self.radio_station,
                                         start="2014-10-25T00:00:00", end="2014-10-25T00:03:00")

    def test_get_song_plays(self):
        data = {"title": 'song_name',
                "performer": 'performer_name',
                "start": '2014-10-21T00:00:00',
                "end": '2014-10-28T00:00:00'}
        response = client.get(reverse('get_songs_plays', kwargs={"song_id": self.song.id}), data)
        self.assertEqual(response.status_code, 200)
