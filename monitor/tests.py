from django.test import TestCase, Client
from django.urls import reverse

from monitor.models import RadioStation, Performer

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




