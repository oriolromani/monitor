from django.test import TestCase, Client
from django.urls import reverse

from monitor.models import RadioStation, Performer, Song, Play

# initialize the APIClient app
client = Client()


class ViewsTestCase(TestCase):
    """
    Test for the monitor api views
    """
    def test_add_channel(self):
        # post with no data
        response = client.post(reverse('add_channel'))
        self.assertEqual(response.status_code, 400)

        # post with data
        data = {"name": "new channel"}
        response = client.post(reverse('add_channel'), data)
        self.assertEqual(response.status_code, 201)
        # one radio station should exist
        self.assertEqual(RadioStation.objects.all().count(), 1)
        # existing radio station should have the data provided in the request
        self.assertTrue(RadioStation.objects.filter(name=data["name"]).exists())
        # if we post again with the same data, as name is unique we should get an error
        response = client.post(reverse('add_channel'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["name"], ['radio station with this name already exists.'])

    def test_add_artist(self):
        # post with no data
        response = client.post(reverse('add_performer'))
        self.assertEqual(response.status_code, 400)

        # post with data
        data = {"name": "new performer"}
        response = client.post(reverse('add_performer'), data)
        self.assertEqual(response.status_code, 201)
        # one radio station should exist
        self.assertEqual(Performer.objects.all().count(), 1)
        # existing radio station should have the data provided in the request
        self.assertTrue(Performer.objects.filter(name=data["name"]).exists())
        # if we post again with the same data, as name is unique we should get an error
        response = client.post(reverse('add_performer'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["name"], ['performer with this name already exists.'])

    def test_add_song(self):
        # post with no data
        response = client.post(reverse('add_song'))
        self.assertEqual(response.status_code, 400)

        # post with missing data
        data = {"title": "new song"}
        response = client.post(reverse('add_song'), data)
        self.assertEqual(response.status_code, 400)

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
        # post with no data
        response = client.post(reverse('add_play'))
        self.assertEqual(response.status_code, 400)

        # post with missing data
        data = {"title": "new song"}
        response = client.post(reverse('add_play'), data)
        self.assertEqual(response.status_code, 400)

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
